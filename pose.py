import cv2
import mediapipe as mp
from config import *
"""
Хэрэгтэй цэгүүд
Баруун гар   12 14 16
Зүүн гар     11 13 15
Баруун хөл   24 26 28
Зүүн хөл     23 25 27
"""


class Pose():
    def __init__(self, mode=False,
                 upper_body=False,
                 smooth=True,
                 d_conf=0.5,
                 t_conf=0.5):
        self.mode = mode
        self.upper_body = upper_body
        self.smooth = smooth
        self.d_conf = d_conf
        self.t_conf = t_conf
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.upper_body, self.smooth)


    def find_pose(self, frame, draw=True):


        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        self.results = self.pose.process(img_rgb)

        if self.results.pose_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(frame, self.results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
        
        return frame

    def get_position(self, frame, draw=True):
        lst = list()
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x*w), int(landmark.y*h)
                lst.append([cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 3, (0, 255, 0), cv2.FILLED)
        return lst
    def get_needed(self, frame, label):
        lst = list()
        if self.results.pose_landmarks:
            for id, landmark in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(landmark.x*w), int(landmark.y*h)
                lst.append([cx, cy])

        file_name = generate()
        
        left_arm_angle_1 = calculate_angle(lst[11], lst[13], lst[15])
        left_arm_angle_2 = calculate_angle(lst[12], lst[11], lst[13])
        right_arm_angle_1 = calculate_angle(lst[12], lst[14], lst[16])
        right_arm_angle_2 = calculate_angle(lst[11], lst[12], lst[14])
        left_leg_angle_1 = calculate_angle(lst[23], lst[25], lst[27])
        left_leg_angle_2 = calculate_angle(lst[24], lst[23], lst[25])
        right_leg_angle_1 = calculate_angle(lst[24], lst[26], lst[28])
        right_leg_angle_2 =  calculate_angle(lst[23], lst[24], lst[26])


        pos = [label,
               str(lst[11][0]), str(lst[11][1]), str(lst[13][0]), str(lst[13][1]), str(lst[15][0]), str(lst[15][1]),
               str(lst[12][0]), str(lst[12][1]), str(lst[14][0]), str(lst[14][1]), str(lst[16][0]), str(lst[16][1]),
               str(lst[23][0]), str(lst[23][1]), str(lst[25][0]), str(lst[25][1]), str(lst[27][0]), str(lst[27][1]),
               str(lst[24][0]), str(lst[24][1]), str(lst[26][0]), str(lst[26][1]), str(lst[28][0]), str(lst[28][1]),
               left_arm_angle_1, left_arm_angle_2,
               right_arm_angle_1, right_arm_angle_2,
               left_leg_angle_1, left_leg_angle_2,
               right_leg_angle_1, right_leg_angle_2,
               file_name,]
        return pos

def main():
    cap = cv2.VideoCapture(0)
    # previous_time = 0
    pose_detector = Pose()
    while True:
        _, frame = cap.read()
        print(frame.shape)
        frame = pose_detector.find_pose(frame, True)
        # lst = pose_detector.get_position(frame, False)
        # current_time = time.time()
        # fps = 1/(current_time - previous_time)
        # previous_time = current_time

        # cv2.putText(frame, str(int(fps)),
        #             (70, 50),
        #             cv2.FONT_HERSHEY_PLAIN,
        #             3,
        #             (255, 0, 0),
        #             3)
        cv2.imshow("Pose", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(1) & 0xFF == ord("s"):
            label = "0"
            # label = input("Enter label of pos: ")
            needed_pos = pose_detector.get_position_needed(frame, label)

            print(f"{needed_pos}")
            dataset_append(needed_pos)
            cv2.imwrite(f"poses/{needed_pos[-1]}.png", frame)
    
if __name__ == "__main__":
    main()