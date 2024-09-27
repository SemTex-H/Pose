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
ALPHABET = ["а", "б", "в", "г", "д",
            "е", "ё", "ж", "з", "и",
            "й", "к", "л", "м", "н",
            "о", "ө", "п", "р", "с",
            "т", "у", "ү", "ф", "х",
            "ц", "ч", "ш", "щ", "ъ",
            "ы", "ь", "э", "ю", "я",
            "+"]

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


def main() -> None:
    last_letter = str()
    message = str()
    message_old = str()
    duplicated_letters = False
    cap = cv2.VideoCapture(0)
    pose_detector = Pose()
    i = 0
    label_i = 60
    while True:
        time.sleep(0.2)
        _, frame = cap.read()

        frame = pose_detector.find_pose(frame, True)
        cv2.imshow("Pose", frame)



        needed_pos = pose_detector.get_position(frame, False)
        angles = calc_angles(needed_pos)
        # print(_right_angle(180, angles[0], 44), _right_angle(90, angles[1], 44))
        
        if _right_angle(angles[2], 135, 20) and _right_angle(angles[6], 135, 20): #Үсэг
            right_hand_point = alphabet_point(angles[4], angles[5])
            left_hand_point = alphabet_point(angles[0], angles[1])
            if right_hand_point >= 0 and left_hand_point >= 0:
                # print("Үсэг", end=':')
                point = right_hand_point + left_hand_point*6

                current_letter = ALPHABET[point]
                if current_letter == ALPHABET[35]:
                    duplicated_letters = True
                elif current_letter != last_letter or duplicated_letters:
                    message += ALPHABET[point]
                    last_letter = current_letter
                    duplicated_letters = False
        if message != message_old:
            print(f"\r{message_old}")
            message_old = message
                # print(point)
        # else: #Тоо болон бусад
        #     right_hand_point = digit_point(angles[4], angles[5])
        #     left_hand_point = digit_point(angles[0], angles[1])
        #     if right_hand_point >= 0 and left_hand_point >= 0:

        #         print("Тоо", end=':')
        #         point = right_hand_point + left_hand_point*4
        #         print(point)

        print(f"\r{message}")


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