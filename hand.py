import cv2
import time
import mediapipe as mp
import math


DEFAULT_LANDMARKS_STYLE = mp.solutions.drawing_styles.get_default_pose_landmarks_style()
DEFAULT_HAND_CONNECTIONS_STYLE = mp.solutions.drawing_styles.get_default_hand_connections_style()

def calculate_angle(landmark1, landmark2, landmark3):
    x1, y1, _ = landmark1
    x2, y2, _ = landmark2
    x3, y3, _ = landmark3

    angle = math.degrees(math.atan(y3-y2, x3-x2) - math.atan(y1-y2, x1-x2))

    return angle+360 if angle < 0 else angle


class Hand():
    def __init__(self, max_hands):
        self.max_hands = max_hands
        self.mp_draw = mp.solutions.drawing_utils
        self.hands = mp.solutions.hands.Hands(max_num_hands=2)


    def find_hand(self, frame, draw=True):

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
          for hand_landmarks in self.results.multi_hand_landmarks:
            if draw:
                self.mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS, DEFAULT_LANDMARKS_STYLE, DEFAULT_HAND_CONNECTIONS_STYLE)
        
        return frame

    def get_position(self, frame, draw=True):
        lst = list()
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                for id, landmark in enumerate(hand_landmarks.landmark):
                    h, w, c = frame.shape
                    cx, cy = int(landmark.x*w), int(landmark.y*h)
                    lst.append([cx, cy])
                    if draw:
                        cv2.circle(frame, (cx, cy), 3, (0, 255, 0), cv2.FILLED)
        return lst
  


def main():
    cap = cv2.VideoCapture(0)
    previous_time = 0
    hand_detector = Hand(2)
    while True:
        success, frame = cap.read()


        frame = hand_detector.find_hand(frame, True)
        lst = hand_detector.get_position(frame, False)
        current_time = time.time()
        fps = 1/(current_time - previous_time)
        previous_time = current_time

        cv2.putText(frame, str(int(fps)),
                    (70, 50),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (255, 0, 0),
                    3)
        cv2.imshow("Pose", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
if __name__ == "__main__":
    main()