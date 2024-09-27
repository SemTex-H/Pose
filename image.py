import cv2

import mediapipe as mp
from pose import Pose
import os
from config import *

lst = os.listdir("D:\\SemTex-H\\Pose\\poses")

def _right_angles(expected_list: list, angle_list: list, sat: int) -> list:
    count =0 
    for i, angle in enumerate(angle_list):
        print(f"comparing {expected_list[i]} to {angle}")
        if expected_list[i]-sat < angle and expected_list[i]+sat > angle:
            count += 1
        else:
            count += 1
    
    return True if count == 8 else False

def _right_angle(expected: int, angle: int, sat: int) -> list:
    if expected-sat < angle and expected+sat > angle:
        return True
    else:
        return False
    
def alphabet_point(angle1: int, angle2: int, sat: int=44)-> int: #Нэг талд тооцоолно
    if _right_angle(180, angle1, sat) and _right_angle(90, angle2, sat):
        return 0
    elif _right_angle(270, angle1, sat) and _right_angle(90, angle2, sat):
        return 1
    elif _right_angle(180, angle1, sat) and _right_angle(180, angle2, sat):
        return 2
    elif _right_angle(90, angle1, sat) and _right_angle(180, angle2, sat):
        return 3
    elif _right_angle(270, angle1, sat) and _right_angle(180, angle2, sat):
        return 4
    elif _right_angle(180, angle1, sat) and _right_angle(270, angle2, sat):
        return 5
    return -1

def digit_point(angle1: int, angle2: int, sat: int=22)-> int: #Нэг талд тооцоолно
    if _right_angle(180, angle1, sat) and _right_angle(90, angle2, sat):
        return 0
    elif _right_angle(180, angle1, sat) and _right_angle(135, angle2, sat):
        return 1
    elif _right_angle(180, angle1, sat) and _right_angle(225, angle2, sat):
        return 2
    elif _right_angle(180, angle1, sat) and _right_angle(270, angle2, sat):
        return 3
    return -1

def main():
    img = cv2.imread(f"D:\\SemTex-H\\Pose\\poses\\{lst[111]}")
    # img = cv2.imread(f'poses/0KpuhwPimx.png')
    print(img.shape)
    img = cv2.resize(img, (640, 480))
    pose_detector = Pose()

    frame = pose_detector.find_pose(img, False)
    cv2.imshow("Pose", frame)

    needed_pos = pose_detector.get_position(frame, False)
    """
    left_elbow, left_shoulder, left_hip, left_knee
    right_elbow, right_shoulder, right_hip, right_knee
    """
    angles = calc_angles(needed_pos)

    # bool_list = _right_angles([90, 180, 90, 180, 180, 90, 90, 180], angles, 44)

    if _right_angle(angles[2], 135, 20) and _right_angle(angles[6], 135, 20): #Үсэг
        right_hand_point = alphabet_point(angles[0], angles[1])
        left_hand_point = alphabet_point(angles[4], angles[5])
        if right_hand_point > 0 and left_hand_point > 0:
            point = right_hand_point + left_hand_point*6
            print(point)
        else:
            print('WRONG POS')

    else: #Тоо болон бусад
        right_hand_point = digit_point(angles[0], angles[1])
        left_hand_point = digit_point(angles[4], angles[5])
        if right_hand_point > 0 and left_hand_point > 0:
            point = right_hand_point + left_hand_point*4
            print(point)
        else:
            print('WRONG POS')



    print(angles)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()