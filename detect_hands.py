import sys
import argparse
import cv2
import mediapipe as mp
import math
from pythonosc import udp_client


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

mp_drawing_styles = mp.solutions.drawing_styles


def detect_hands(osc_ip, osc_port):
    client = udp_client.SimpleUDPClient(osc_ip, osc_port)

    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=10,
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands_model:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            results = hands_model.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                number_of_hands = len(results.multi_hand_landmarks)
                client.send_message("/number_of_hands", number_of_hands)

                for hand_index, hand_landmarks in enumerate(
                    results.multi_hand_landmarks
                ):
                    hand_landmarks_list = list(hand_landmarks.landmark)
                    wrist = hand_landmarks_list[mp_hands.HandLandmark.WRIST]
                    normalized_x = wrist.x
                    normalized_y = wrist.y
                    # print(wrist.x, wrist.y, normalized_x, normalized_y)
                    client.send_message("/hand", [hand_index, wrist.x, wrist.y])

                    image_width = image.shape[1]
                    image_height = image.shape[0]
                    wrist_x_px = min(
                        math.floor(normalized_x * image_width), image_width - 1
                    )
                    wrist_y_py = min(
                        math.floor(normalized_y * image_height), image_height - 1
                    )
                    cv2.circle(image, (wrist_x_px, wrist_y_py), 5, (0, 0, 255), -1)

            cv2.imshow("MediaPipe Hands", image)
            if cv2.waitKey(5) & 0xFF == 27:
                break


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
    parser.add_argument(
        "--port", type=int, default=5005, help="The port the OSC server is listening on"
    )
    args = parser.parse_args()
    detect_hands(args.ip, args.port)
