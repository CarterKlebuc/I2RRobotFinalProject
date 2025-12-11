#include "PoseEstimation.h"

float joint_angles[3];

void setup() {
  setup_sensors();
  Serial.begin(115200);
  randomSeed(analogRead(0));
}

void loop() {
  read_joint_angles(joint_angles);
  Serial.println("=== Joint Angles ===");
  Serial.print("q1 (rad,deg) = ");
  Serial.print(joint_angles[0], 2); Serial.println(" deg)");

  Serial.print("q2 (rad,deg) = ");
  Serial.print(joint_angles[1], 2); Serial.println(" deg)");

  Serial.print("q3 (rad,deg) = ");
  Serial.print(joint_angles[2], 2); Serial.println(" deg)");

  Serial.print(random(1, 1000));

  Serial.println();

  delay(50);  // ~20 Hz
}