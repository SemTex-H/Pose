import cv2
import time
import mediapipe as mp
import math
import pandas as pd
import csv
from config import *

from pose import Pose
"""
Хэрэгтэй цэгүүд
Баруун гар   12 14 16
Зүүн гар     11 13 15
Баруун хөл   24 26 28
Зүүн хөл     23 25 27
"""

def _right_angle(expected_list: list, angle_list: list, sat: int) -> list:
    bool_list = list()
    for i, angle in enumerate(angle_list):
        if expected_list[i]-sat < angle and expected_list[i]+sat > angle:
            bool_list.append(True)
        else:
            bool_list.append(False)
    return bool_list


def main() -> None:
    cap = cv2.VideoCapture(0)
    pose_detector = Pose()
    i = 0
    label_i = 60
    while True:
        _, frame = cap.read()

        frame = pose_detector.find_pose(frame, True)
        cv2.imshow("Pose", frame)



        pressedKey = cv2.waitKey(1) & 0xFF
        if pressedKey & 0xFF == ord("q"):
            break
        elif pressedKey & 0xFF == ord("l"):
            label = str(label_i)
            needed_pos = pose_detector.get_needed(frame, label)
            dataset_append(needed_pos)
            cv2.imwrite(f"poses/{needed_pos[-1]}.png", frame)
            i+=1
            print(f"label_{label}_{i} published.")
    
if __name__ == "__main__":
    main()