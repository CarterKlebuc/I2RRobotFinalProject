#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>

// TCA9548A I2C multiplexer (needed because all BNOs share same I2C address)
#define TCA_ADDR 0x70

// BNO055 I2C address (default 0x28 or 0x29)
#define BNO_ADDR 0x28

// We have 3 sensors: base, link1, link2
const int NUM_SENSORS = 3;

// BNO objects (same I2C addr, but we select them by TCA channel)
Adafruit_BNO055 bno[NUM_SENSORS] = {
  Adafruit_BNO055(0, BNO_ADDR),  // Sensor 0: base
  Adafruit_BNO055(1, BNO_ADDR),  // Sensor 1: link1 (upper arm)
  Adafruit_BNO055(2, BNO_ADDR)   // Sensor 2: link2 (forearm)
};

// Link 1 is 9 [mm]
// Link 2 is 7 [mm] to IMU and 12 [mm] to end effector

// ================== DH PARAMETERS (PLACEHOLDERS) ==================
// Standard DH for 3-DOF arm, adjust for your robot.
// Joint variables are q[0..2] (radians).
float dh_a[3]      = {0.10f, 0.10f, 0.10f};  // link lengths (m)
float dh_alpha[3]  = {0.0f,  0.0f,  0.0f};   // link twists (rad)
float dh_d[3]      = {0.0f,  0.0f,  0.0f};   // link offsets (m)
// Offset between IMU-based joint angle and DH zero:
float theta_offset[3] = {0.0f, 0.0f, 0.0f};

// ================== SENSOR→LINK CALIBRATION ==================
// R_S_L[i] is 3x3 rotation that takes vectors from sensor i frame → link i frame.
//
// Index 0 = base, 1 = link1, 2 = link2.
// Start with identity and later fill with your calibration.
float R_S_L[NUM_SENSORS][3][3] = {
  // Sensor 0 on base
  {
    {1.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 1.0f}
  },
  // Sensor 1 on link1 (upper arm)
  {
    {1.0f, 0.0f, 0.0f},
    {0.f, 1.0f, 0.0f},
    {0.0f, 0.0f, 1.0f}
  },
  // Sensor 2 on link2 (forearm)
  {
    {1.0f, 0.0f, 0.0f},
    {0.0f, 1.0f, 0.0f},
    {0.0f, 0.0f, 1.0f}
  }
};

// ================== MATH HELPERS ==================

void tcaSelect(uint8_t i) {
  if (i > 7) return;
  Wire.beginTransmission(TCA_ADDR);
  Wire.write(1 << i);
  Wire.endTransmission();
}

// quaternion → rotation matrix, world←sensor (R_W_S)
//
// Quaternion convention from Adafruit_BNO055 is (w, x, y, z).
void quatToMatrix(float w, float x, float y, float z, float R[3][3]) {
  // Normalize just in case
  float n = sqrtf(w*w + x*x + y*y + z*z);
  if (n > 0.0f) {
    w /= n; x /= n; y /= n; z /= n;
  }

  float ww = w*w, xx = x*x, yy = y*y, zz = z*z;
  float wx = w*x, wy = w*y, wz = w*z;
  float xy = x*y, xz = x*z, yz = y*z;

  R[0][0] = 1.0f - 2.0f*(yy + zz);
  R[0][1] = 2.0f*(xy - wz);
  R[0][2] = 2.0f*(xz + wy);

  R[1][0] = 2.0f*(xy + wz);
  R[1][1] = 1.0f - 2.0f*(xx + zz);
  R[1][2] = 2.0f*(yz - wx);

  R[2][0] = 2.0f*(xz - wy);
  R[2][1] = 2.0f*(yz + wx);
  R[2][2] = 1.0f - 2.0f*(xx + yy);
}

void matMul3(const float A[3][3], const float B[3][3], float C[3][3]) {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      C[i][j] = 0.0f;
      for (int k = 0; k < 3; k++) {
        C[i][j] += A[i][k] * B[k][j];
      }
    }
  }
}

void matTranspose3(const float A[3][3], float AT[3][3]) {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
      AT[i][j] = A[j][i];
    }
  }
}

// Extract angle of a rotation that is (mostly) a pure rotation around the Y axis.
// For ideal R_y(theta):
// R = [ cosθ  0  sinθ
//       0     1   0
//      -sinθ  0  cosθ ]
// θ = atan2(R[0][2], R[0][0]).
float angleFromRotAboutY(const float R[3][3]) {
  return atan2f(R[0][2], R[0][0]);
}

// Yaw (heading) from world→base rotation matrix (Z-up, yaw about Z).
// For Rz(yaw), yaw = atan2(R[1][0], R[0][0]).
float yawFromRotation(const float R[3][3]) {
  return atan2f(R[1][0], R[0][0]);
}

// ================== SETUP ==================

void setup_sensors() {
  Serial.begin(115200);
  while (!Serial) { delay(10); }

  Wire.begin();

  Serial.println("Initializing 3x BNO055...");

  for (int i = 0; i < NUM_SENSORS; i++) {
    tcaSelect(i);    // select TCA channel for this sensor

    if (!bno[i].begin()) {
      Serial.print("Failed to init BNO055 #");
      Serial.println(i);
      while (1) { delay(10); }
    }

    bno[i].setExtCrystalUse(true);
    delay(50);
  }

  Serial.println("BNO055 init complete.\n");
  Serial.end();
}

// ================== MAIN LOOP ==================

void read_joint_angles(float joint_angles[3]) {
  // 1) Read heading/roll/pitch + quaternion from each sensor
  float heading_deg[NUM_SENSORS];
  float roll_deg[NUM_SENSORS];
  float pitch_deg[NUM_SENSORS];

  float R_W_S[NUM_SENSORS][3][3];  // world->sensor rotation

  for (int i = 0; i < NUM_SENSORS; i++) {
    tcaSelect(i);

    // Euler angles (for debug / printing)
    imu::Vector<3> euler = bno[i].getVector(Adafruit_BNO055::VECTOR_EULER);
    // Adafruit: euler.x = heading, euler.y = roll, euler.z = pitch (degrees)
    heading_deg[i] = euler.x();
    roll_deg[i]    = euler.y();
    pitch_deg[i]   = euler.z();

    // Quaternion for robust orientation math
    imu::Quaternion quat = bno[i].getQuat();
    float w = quat.w();
    float x = quat.x();
    float y = quat.y();
    float z = quat.z();

    quatToMatrix(w, x, y, z, R_W_S[i]);
  }

  // 2) Apply sensor→link calibration: R_W_L = R_W_S * R_S_L
  // Links: 0 = base, 1 = link1, 2 = link2
  float R_W_L[3][3][3];
  for (int i = 0; i < NUM_SENSORS; i++) {
    matMul3(R_W_S[i], R_S_L[i], R_W_L[i]);
  }

  // 3) Compute joint angles
  // Joint 1: yaw of base relative to world (Z axis)
  float q1 = yawFromRotation(R_W_L[0]);

  // Joint 2: pitch about Y between base and link1
  float R_W_L0_T[3][3], R_W_L1_T[3][3];
  float R_L0_L1[3][3];

  matTranspose3(R_W_L[0], R_W_L0_T);
  matTranspose3(R_W_L[1], R_W_L1_T);

  // Relative rotation from base (0) to link1 (1)
  matMul3(R_W_L0_T, R_W_L[1], R_L0_L1);
  float q2 = angleFromRotAboutY(R_L0_L1);

  // Joint 3: pitch about Y between link1 and link2
  float R_L1_L2[3][3];
  matMul3(R_W_L1_T, R_W_L[2], R_L1_L2);
  float q3 = angleFromRotAboutY(R_L1_L2);

  // 4) Apply DH offsets if needed
  float q[3];
  q[0] = q1 + theta_offset[0];
  q[1] = q2 + theta_offset[1];
  q[2] = q3 + theta_offset[2];

  // 5) Print everything
  const float RAD2DEG = 180.0f / PI;

  joint_angles[0] = q1 * RAD2DEG;
  joint_angles[1] = q2 * RAD2DEG;
  joint_angles[2] = q3 * RAD2DEG;
}
