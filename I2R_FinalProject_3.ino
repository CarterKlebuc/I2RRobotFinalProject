#include <Wire.h>
#include "PoseEstimation.h"
#include <Adafruit_MotorShield.h>

// ====== SHIELD ======
Adafruit_MotorShield AFMS = Adafruit_MotorShield(0x60);

// ====== MOTOR MAPPING ======
Adafruit_DCMotor* M_BASE     = AFMS.getMotor(1); // base rotation
Adafruit_DCMotor* M_SHOULDER = AFMS.getMotor(2); // shoulder
Adafruit_DCMotor* M_ELBOW    = AFMS.getMotor(3); // elbow

// ====== PID GAINS ======
float Kp_base = 5.0, Ki_base = 0.8, Kd_base = 1.0;
float Kp_sho  = 5.0, Ki_sho  = 1.2, Kd_sho  = 1.0;
float Kp_elb  = 5.0, Ki_elb  = 1.5, Kd_elb  = 1.0;

// ====== SETPOINTS (degrees) ======
float ref_base     = 87.0;
float ref_shoulder = 90.0;
float ref_elbow    = 100.0;

// ====== PID States ======
float e_base = 0, e_base_prev = 0, int_base = 0;
float e_sho  = 0, e_sho_prev  = 0, int_sho  = 0;
float e_elb  = 0, e_elb_prev  = 0, int_elb  = 0;

unsigned long lastTime = 0;

// ====== BOUNDS ======
const float INT_LIM = 200.0;    // Anti-windup
const int   PWM_MAX = 255;
const int   DEADBAND_PWM = 20;  // Dead Zone

float joint_angles[3];

void setMotorPID(Adafruit_DCMotor* m, float u);

// ================== SETUP ==================
void setup() { 
  AFMS.begin();   

  lastTime = millis();

  setup_sensors();
  Serial.begin(115200);\
  randomSeed(analogRead(0));

  // BASE
  Serial.println("Type q1 Setpoint: ");
  while (Serial.available() == 0) {}
  ref_base = Serial.parseFloat();
  while (Serial.available() > 0) Serial.read();
  Serial.print("BASE setpoint = ");
  Serial.println(ref_base);
  delay(300);

  // SHOULDER
  Serial.println("Type q2 Setpoint: ");
  while (Serial.available() == 0) {}
  ref_shoulder = Serial.parseFloat();
  while (Serial.available() > 0) Serial.read();
  Serial.print("SHOULDER setpoint = ");
  Serial.println(ref_shoulder);
  delay(300);

  // ELBOW
  Serial.println("Type q3 Setpoint: ");
  while (Serial.available() == 0) {}
  ref_elbow = Serial.parseFloat();
  while (Serial.available() > 0) Serial.read();
  Serial.print("ELBOW setpoint = ");
  Serial.println(ref_elbow);
  delay(300);
}

// ================== LOOP ==================
void loop() {

  unsigned long now = millis();
  float dt = (now - lastTime) / 1000.0;  // s
  if (dt <= 0.0) dt = 0.001;
  lastTime = now;  


  read_joint_angles(joint_angles);

  float ang_base     = joint_angles[0];
  float ang_shoulder = joint_angles[1];
  float ang_elbow    = joint_angles[2];

  e_base = ref_base - ang_base;
  e_sho  = ref_shoulder - ang_shoulder;
  e_elb  = ref_elbow - ang_elbow;

  int_base += e_base * dt;
  if (int_base > INT_LIM)  int_base = INT_LIM;
  if (int_base < -INT_LIM) int_base = -INT_LIM;

  int_sho += e_sho * dt;
  if (int_sho > INT_LIM)  int_sho = INT_LIM;
  if (int_sho < -INT_LIM) int_sho = -INT_LIM;

  int_elb += e_elb * dt;
  if (int_elb > INT_LIM)  int_elb = INT_LIM;
  if (int_elb < -INT_LIM) int_elb = -INT_LIM;

  float der_base = (e_base - e_base_prev) / dt;
  float der_sho  = (e_sho  - e_sho_prev)  / dt;
  float der_elb  = (e_elb  - e_elb_prev)  / dt;

  e_base_prev = e_base;
  e_sho_prev  = e_sho;
  e_elb_prev  = e_elb;

  // ---- PID ----
  float u_base = Kp_base * e_base + Ki_base * int_base + Kd_base * der_base;
  float u_sho  = Kp_sho  * e_sho  + Ki_sho  * int_sho  + Kd_sho  * der_sho;
  float u_elb  = Kp_elb  * e_elb  + Ki_elb  * int_elb  + Kd_elb  * der_elb;
  
  setMotorPID(M_BASE,     u_base);
  setMotorPID(M_SHOULDER, u_sho);
  setMotorPID(M_ELBOW,    u_elb);

  Serial.print("q1 - Ref: ");
  Serial.print(ref_base);
  Serial.print("  Angle: ");
  Serial.print(ang_base);
  Serial.print("  U: ");
  Serial.print(u_base);

  Serial.print("   q2 - Ref: ");
  Serial.print(ref_shoulder);
  Serial.print("  Angle: ");
  Serial.print(ang_shoulder);
  Serial.print("  U: ");
  Serial.print(u_sho);

  Serial.print("   q3 - Ref: ");
  Serial.print(ref_elbow);
  Serial.print("  Angle: ");
  Serial.print(ang_elbow);
  Serial.print("  U: ");
  Serial.println(u_elb);
  
}


void setMotorPID(Adafruit_DCMotor* m, float u) {
  if (u >  PWM_MAX) u =  PWM_MAX;
  if (u < -PWM_MAX) u = -PWM_MAX;

  float mag = fabs(u);
  uint8_t pwm = (uint8_t)mag;
  Serial.println(pwm);

  if (pwm < DEADBAND_PWM) {
    m->run(RELEASE);
    m->setSpeed(0);
    return;
  }

  if (u > 0) {
    m->run(FORWARD);
  } else {
    m->run(BACKWARD);
  }
  m->setSpeed(pwm);
}
