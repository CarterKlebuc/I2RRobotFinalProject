import time
import math
from dataclasses import dataclass
from typing import List, Tuple
from LetterValues import *

from rtde_receive import RTDEReceiveInterface as RTDEReceive
from rtde_control import RTDEControlInterface as RTDEControl

ROBOT_IP = "192.168.0.10"

# Conservative settings
SPEED_M_S = 0.60
ACC_M_S2 = 0.80
POS_TOL_M = 0.003
TIMEOUT_S = 20.0


def fmt_pose(p: List[float]) -> str:
    return (
        f"XYZ (m):  x={p[0]: .4f}, y={p[1]: .4f}, z={p[2]: .4f} | "
        f"Rvec (rad): rx={p[3]: .4f}, ry={p[4]: .4f}, rz={p[5]: .4f}"
    )


def rpy_deg_to_rotvec_rad(roll_deg: float, pitch_deg: float, yaw_deg: float) -> Tuple[float, float, float]:
    """Convert roll/pitch/yaw in degrees to UR rotation-vector (axis-angle) in radians.
       Uses R = Rz(yaw) * Ry(pitch) * Rx(roll).
    """
    r = math.radians(roll_deg)
    p = math.radians(pitch_deg)
    y = math.radians(yaw_deg)

    cr, sr = math.cos(r), math.sin(r)
    cp, sp = math.cos(p), math.sin(p)
    cy, sy = math.cos(y), math.sin(y)

    # Rotation matrix R = Rz(y) * Ry(p) * Rx(r)
    R00 = cy * cp
    R01 = cy * sp * sr - sy * cr
    R02 = cy * sp * cr + sy * sr

    R10 = sy * cp
    R11 = sy * sp * sr + cy * cr
    R12 = sy * sp * cr - cy * sr

    R20 = -sp
    R21 = cp * sr
    R22 = cp * cr

    # Axis-angle from rotation matrix
    trace = R00 + R11 + R22
    cos_theta = max(-1.0, min(1.0, (trace - 1.0) / 2.0))
    theta = math.acos(cos_theta)

    if abs(theta) < 1e-9:
        return (0.0, 0.0, 0.0)

    # For numerical stability when theta ~ pi
    sin_theta = math.sin(theta)
    if abs(sin_theta) < 1e-9:
        # Fallback: pick axis from diagonal
        # (This is rare; good enough for typical lab orientations.)
        ax = math.sqrt(max(0.0, (R00 + 1) / 2))
        ay = math.sqrt(max(0.0, (R11 + 1) / 2))
        az = math.sqrt(max(0.0, (R22 + 1) / 2))
        return (ax * theta, ay * theta, az * theta)

    ax = (R21 - R12) / (2.0 * sin_theta)
    ay = (R02 - R20) / (2.0 * sin_theta)
    az = (R10 - R01) / (2.0 * sin_theta)

    # Rotation vector = axis * angle
    return (ax * theta, ay * theta, az * theta)


def wait_reached_xyz(rtde_r: RTDEReceive, target_xyz, timeout_s: float) -> bool:
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        p = rtde_r.getActualTCPPose()
        if math.dist([p[0], p[1], p[2]], list(target_xyz)) <= POS_TOL_M:
            return True
        time.sleep(0.02)
    return False


def movel_to_xyz_with_rpy_deg(target_xyz, roll_deg, pitch_deg, yaw_deg):
    rtde_r = RTDEReceive(ROBOT_IP)
    rtde_c = RTDEControl(ROBOT_IP)

    try:
        # Default TCP (flange)
        rtde_c.setTcp([0, 0, 0, 0, 0, 0])

        # Print current pose BEFORE moving
        cur_pose = rtde_r.getActualTCPPose()
        print("Current TCP pose:", fmt_pose(cur_pose))

        rx, ry, rz = rpy_deg_to_rotvec_rad(roll_deg, pitch_deg, yaw_deg)
        tx, ty, tz = target_xyz
        target_pose = [tx, ty, tz, rx, ry, rz]

        print(f"Commanded orientation (RPY deg): roll={roll_deg}, pitch={pitch_deg}, yaw={yaw_deg}")
        print("Commanded TCP pose:", fmt_pose(target_pose))

        # Optional IK pre-check (clean failure if impossible)
        if hasattr(rtde_c, "getInverseKinematics"):
            q_seed = rtde_r.getActualQ()
            try:
                q = rtde_c.getInverseKinematics(target_pose, q_seed)
            except TypeError:
                q = rtde_c.getInverseKinematics(target_pose)

            if q is None or len(q) != 6:
                raise RuntimeError("IK failed for XYZ + requested RPY(deg). Try a different XYZ or orientation.")

        # MoveL (straight Cartesian line)
        ok = rtde_c.moveL(target_pose, SPEED_M_S, ACC_M_S2)
        if not ok:
            raise RuntimeError("moveL returned False (command rejected or robot stopped).")

        if not wait_reached_xyz(rtde_r, (tx, ty, tz), TIMEOUT_S):
            raise RuntimeError("Timed out reaching target XYZ (possible stop or very slow move).")

        final_pose = rtde_r.getActualTCPPose()
        print("Final TCP pose:", fmt_pose(final_pose))

    finally:
        try:
            rtde_c.stopScript()
        except Exception:
            pass


def test_bounds():
    top_bound = 0.4509
    middle_not_bound = 0.3509
    bottom_bound = 0.2509
    right_bound = -0.2509
    left_bound = 0.2509
    # Testing Move Up
    l_top_penup_bound = (pen_up, 0, top_bound)
    l_top_pendown_bound = (pen_down, 0, top_bound)
    # Testing Move Down
    l_bottom_penup_bound = (pen_up, 0, bottom_bound)
    l_bottom_pendown_bound = (pen_down, 0, bottom_bound)
    # Testing Move Left
    l_left_penup_bound = (pen_up, left_bound, middle_not_bound)
    l_left_pendown_bound = (pen_down, left_bound, middle_not_bound)
    # Testing Move Right
    l_right_penup_bound = (pen_up, right_bound, middle_not_bound)
    l_right_pendown_bound = (pen_down, right_bound, middle_not_bound)
    movel_to_xyz_with_rpy_deg(l_top_penup_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_top_pendown_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_bottom_penup_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_bottom_pendown_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_left_penup_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_left_pendown_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_right_penup_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_right_pendown_bound, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)


def write_l():
    # Need to write an L from the home pose
    l_top_base_penup = (pen_up, 0, 0.4509)
    l_top_base_pendown = (pen_down, 0, 0.4509)
    l_bottom_base_move_down_pendown = (pen_down, 0, 0.2509)
    l_bottom_base_move_right_pendown = (pen_down, -0.0885, 0.2509)
    l_bottom_base_move_right_penup = (pen_up, -0.0285, 0.2509)
    movel_to_xyz_with_rpy_deg(l_top_base_penup, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_top_base_pendown, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_bottom_base_move_down_pendown, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_bottom_base_move_right_pendown, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(l_bottom_base_move_right_penup, roll_deg, pitch_deg, yaw_deg)
    movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)


# Target XYZ in meters
pen_up = 0.3064
pen_down = 0.3264
home_position = (pen_up, -0.0285, 0.3509)

# Desired TCP orientation as RPY in DEGREES
roll_deg = 0.0
pitch_deg = 90.0
yaw_deg = 0.0

movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)
should_plot_letter = True

'''
For robot movement:
Middle: (x = 0, y = 0.3500)
Vertical Bounds: 0.2500 to 0.4500

Horizontal Bounds: 0.2500 to -0.2500

Vert: 0.10
Horizontal: 0.25

For creating a letter.
Middle: (x = 0, y = 0)
Max units should be -5 to 5 for vert and horizontal
Movement of 1 equals 0.02 for vertical movement and 0.05 for horizontal movement

functions:
    - horizontal: h(x) = -x * 0.05
    - vertical: v(x) = (x * 0.02) + 0.35
'''



def letter_to_robot_space(letter_coordinates):
    horizontal_coefficient = 0.025
    vertical_coefficient = 0.025
    if (abs(letter_coordinates[1]) <= 5) and (abs(letter_coordinates[2]) <= 5):
        final_tuple = (letter_coordinates[0], letter_coordinates[1] * -horizontal_coefficient, (letter_coordinates[2] * vertical_coefficient) + 0.35)
        return final_tuple
    print("Error: X and Y letter coordinates cannot be greater than 5!")
    null_tuple = (0, 0, 0)
    return null_tuple

def plot_word(word):
    if len(word) <= 4:
        letter_list = list(word)
        spacing = (5 - len(word)) / len(word)
        offsets = [-4, -1, 2, 4]
        counter = 0
        for letter in letter_list:
            letter_points = letter_equivalent_values[letter]
            # Move to Home Position with pen up
            movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)
            # Move to Letter Starting Position with pen up
            letter_starting_position = (pen_up, letter_points[0][0] + offsets[counter], letter_points[0][1])
            letter_starting_position = letter_to_robot_space(letter_starting_position)
            movel_to_xyz_with_rpy_deg(letter_starting_position, roll_deg, pitch_deg, yaw_deg)
            # Cycle through letter points with pen down
            for point in letter_points:
                letter_current_position = (point[2], point[0] + offsets[counter], point[1])
                letter_current_position = letter_to_robot_space(letter_current_position)
                movel_to_xyz_with_rpy_deg(letter_current_position, roll_deg, pitch_deg, yaw_deg)
            # Move to last letter position with pen up
            letter_current_position = (pen_down, letter_points[-1][0] + offsets[counter], letter_points[-1][1])
            letter_current_position = letter_to_robot_space(letter_current_position)
            movel_to_xyz_with_rpy_deg(letter_current_position, roll_deg, pitch_deg, yaw_deg)
            # Move back to home position
            movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)
            counter += 1
    print("Word cannot be greater than 4 characters!")

def plot_letter(letter):
    if letter != "S":
        letter_points = letter_equivalent_values[letter]
        # Move to Home Position with pen up
        movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)
        # Move to Letter Starting Position with pen up
        letter_starting_position = (pen_up, letter_points[0][0], letter_points[0][1])
        letter_starting_position = letter_to_robot_space(letter_starting_position)
        movel_to_xyz_with_rpy_deg(letter_starting_position, roll_deg, pitch_deg, yaw_deg)
        # Cycle through letter points with pen down
        for point in letter_points:
            letter_current_position = (point[2], point[0], point[1])
            letter_current_position = letter_to_robot_space(letter_current_position)
            movel_to_xyz_with_rpy_deg(letter_current_position, roll_deg, pitch_deg, yaw_deg)
        # Move to last letter position with pen up
        letter_current_position = (pen_down, letter_points[-1][0], letter_points[-1][1])
        letter_current_position = letter_to_robot_space(letter_current_position)
        movel_to_xyz_with_rpy_deg(letter_current_position, roll_deg, pitch_deg, yaw_deg)
        # Move back to home position
        movel_to_xyz_with_rpy_deg(home_position, roll_deg, pitch_deg, yaw_deg)
    else:
        plot_word("SOS")

