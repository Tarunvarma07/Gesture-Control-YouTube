import cv2
import mediapipe as mp
import numpy as np
import time
import pyautogui

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Configure pyautogui fail-safe and pause
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1

# Utility Functions for Gesture Recognition
def fingers_up(hand_landmarks, handedness='Right'):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if handedness == 'Right':
        fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0] - 1].x else 0)

    # Other fingers
    for idx in range(1, 5):
        fingers.append(
            1 if hand_landmarks.landmark[tips_ids[idx]].y < hand_landmarks.landmark[tips_ids[idx] - 2].y
            else 0
        )

    return fingers

def is_fist(fingers_status):
    return sum(fingers_status) == 0

def is_palm(fingers_status):
    return sum(fingers_status) == 5

def is_thumbs_up(hand_landmarks, fingers_status):
    return fingers_status[0] == 1 and sum(fingers_status[1:]) == 0 and hand_landmarks.landmark[4].y < hand_landmarks.landmark[0].y

def is_thumbs_down(hand_landmarks, fingers_status):
    return fingers_status[0] == 1 and sum(fingers_status[1:]) == 0 and hand_landmarks.landmark[4].y > hand_landmarks.landmark[0].y

def is_index_pointing(fingers_status):
    return fingers_status == [0, 1, 0, 0, 0]

def is_peace(fingers_status):
    return fingers_status == [0, 1, 1, 0, 0]

def is_rock_sign(fingers_status):
    # Thumb down (0) and all other four fingers up (sum == 4)
    return fingers_status[0] == 0 and sum(fingers_status[1:]) == 4

class Cooldown:
    def __init__(self, cooldown_time=1.0):
        self.cooldown_time = cooldown_time
        self.last_trigger = 0

    def ready(self):
        return time.time() - self.last_trigger > self.cooldown_time

    def trigger(self):
        self.last_trigger = time.time()

# Set cooldowns per gesture
cooldowns = {
    'palm': Cooldown(2.0),
    'fist': Cooldown(2.0),
    'thumbs_up': Cooldown(0.2),
    'thumbs_down': Cooldown(0.3),
    'index_pointing': Cooldown(0.9),
    'peace': Cooldown(0.9),
    'rock': Cooldown(3.0),
}

def main():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.6
    ) as hands:

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                handedness = results.multi_handedness[0].classification[0].label

                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fs = fingers_up(hand_landmarks, handedness)

                # Debug print
                print(f"Fingers: {fs}")

                # Gesture → Action
                if is_palm(fs) and cooldowns['palm'].ready():
                    pyautogui.press('space')
                    cooldowns['palm'].trigger()
                    cv2.putText(frame, "Play/Pause", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

                elif is_fist(fs) and cooldowns['fist'].ready():
                    pyautogui.press('m')
                    cooldowns['fist'].trigger()
                    cv2.putText(frame, "Mute/Unmute", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

                elif is_thumbs_up(hand_landmarks, fs) and cooldowns['thumbs_up'].ready():
                    pyautogui.press('volumeup')
                    cooldowns['thumbs_up'].trigger()
                    cv2.putText(frame, "Volume Up", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

                elif is_thumbs_down(hand_landmarks, fs) and cooldowns['thumbs_down'].ready():
                    pyautogui.press('volumedown')
                    cooldowns['thumbs_down'].trigger()
                    cv2.putText(frame, "Volume Down", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,0), 2)

                elif is_index_pointing(fs) and cooldowns['index_pointing'].ready():
                    pyautogui.press('right')
                    cooldowns['index_pointing'].trigger()
                    cv2.putText(frame, "Seek Forward", (10, 170), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                elif is_peace(fs) and cooldowns['peace'].ready():
                    pyautogui.press('left')
                    cooldowns['peace'].trigger()
                    cv2.putText(frame, "Seek Backward", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

                elif is_rock_sign(fs) and cooldowns['rock'].ready():
                    print("Rock detected → Next Song")
                    pyautogui.hotkey('shift', 'n')  # Fixed: Use Shift+N for YouTube
                    cooldowns['rock'].trigger()
                    cv2.putText(frame, "Next Song", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 1, (200,0,200), 2)

            cv2.imshow('YouTube Gesture Control', frame)

            # Exit on 'e'
            if cv2.waitKey(5) & 0xFF == ord('e'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
