import string
import os
import secrets
import math
import pandas as pd
letters = string.ascii_letters
digits = string.digits

selection = letters + digits

password_len = 10

def names():
    password = ''
    for i in range(password_len):
        password += ''.join(secrets.choice(selection))

    return password

def generate():
    name = names()
    while os.path.isfile(f"poses//{name}.png"):
        name = names()
    return name

def calculate_angle(landmark1, landmark2, landmark3):
    x1, y1 = landmark1
    x2, y2 = landmark2
    x3, y3 = landmark3

    angle = math.degrees(math.atan2(y3-y2, x3-x2) - math.atan2(y1-y2, x1-x2))

    return int(angle+360) if angle < 0 else int(angle)


def calc_angles(lst: list):
    left_elbow = calculate_angle(lst[15], lst[13], lst[11])
    left_shoulder = calculate_angle(lst[13], lst[11], lst[12])
    right_elbow = calculate_angle(lst[12], lst[14], lst[16])
    right_shoulder = calculate_angle(lst[11], lst[12], lst[14])
    left_knee = calculate_angle(lst[27], lst[25], lst[23])
    left_hip = calculate_angle(lst[25], lst[23], lst[24])
    right_knee = calculate_angle(lst[24], lst[26], lst[28])
    right_hip = calculate_angle(lst[23], lst[24], lst[26])
    return [left_elbow, left_shoulder, left_hip, left_knee, 
            right_elbow, right_shoulder, right_hip, right_knee]

def dataset_append(lst):
    names = ['label',
             'left_arm_1_x','left_arm_1_y','left_arm_2_x','left_arm_2_y','left_arm_3_x','left_arm_3_y',
             'right_arm_1_x','right_arm_1_y','right_arm_2_x','right_arm_2_y','right_arm_3_x','right_arm_3_y',
             'left_leg_1_x','left_leg_1_y','left_leg_2_x','left_leg_2_y','left_leg_3_x','left_leg_3_y',
             'right_leg_1_x','right_leg_1_y','right_leg_2_x','right_leg_2_y','right_leg_3_x','right_leg_3_y',
             'left_arm_angle_1', 'left_arm_angle_2',
             'right_arm_angle_1', 'right_arm_angle_2',
             'left_leg_angle_1', 'left_leg_angle_2',
             'right_leg_angle_1', 'right_leg_angle_2',
             'image_path']
    nested_lst = [[i] for i in lst]
    # return dict(zip(names, nested_lst))
    df = pd.DataFrame(dict(zip(names, nested_lst)))

    df.to_csv('dataset.csv', mode='a', index=False, header=False)

if __name__ == "__main__":
    lst =['9', '301', '127', '312', '198', '298', '253', '213', '114', '185', '183', '185', '247', '267', '263', '258', '351', '248', '436', '213', '256', '201', '341', '187', '424', '1234']
    dataset_append(lst)


