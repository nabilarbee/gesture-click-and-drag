import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

# use mediapipie hands solution
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# note: adjust the confidence if your camera is not good enough
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,              # configure other number if you wanna change amount of maximum hands
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# get screen size for moving the mouse pointer
screen_width, screen_height = pyautogui.size()

# adjust control box if needed, this is the area where hand movements are tracked
CONTROL_BOX_MARGIN = 100

# threshold distance for recognising click and drag gestures
GESTURE_DISTANCE_THRESHOLD = 40

# currently using 0 for default webcams, if you have other webcams please change it to 1, 2, or other numbers accordingly
cap = cv2.VideoCapture(0)
click_lock = False
drag_state = "IDLE"

print("To quit, press 'q'.")

while cap.isOpened():
    # for each frame CAPTURED in camera
    success, frame = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # change 1 to 0 if you dont want a mirrored view
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    cv2.rectangle(frame, (CONTROL_BOX_MARGIN, CONTROL_BOX_MARGIN), 
                  (frame_width - CONTROL_BOX_MARGIN, frame_height - CONTROL_BOX_MARGIN), 
                  (255, 255, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            
            # drawing the hand landmarks on frame
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=hand_landmarks,
                connections=mp_hands.HAND_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=2, circle_radius=4),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2)
            )
            # print(hand_handedness.classification[0].label)

            # handedness has the label of left or right hand and many other classifications, read the docs for the rest if needed
            hand_label = hand_handedness.classification[0].label
            # if left hand
            if hand_label == 'Left':
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
                middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)
                cv2.circle(frame, (middle_x, middle_y), 10, (0, 255, 255), cv2.FILLED)
                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), cv2.FILLED)
                distanceLeft = math.hypot(index_x - middle_x, index_y - middle_y)
                middle_x_cam = int(middle_tip.x * frame_width)
                middle_y_cam = int(middle_tip.y * frame_height)
                screen_x = np.interp(middle_x_cam, [CONTROL_BOX_MARGIN, frame_width - CONTROL_BOX_MARGIN], [0, screen_width])
                screen_y = np.interp(middle_y_cam, [CONTROL_BOX_MARGIN, frame_height - CONTROL_BOX_MARGIN], [0, screen_height])
                # move mouse only if fingers are close enough
                if distanceLeft < GESTURE_DISTANCE_THRESHOLD:
                    pyautogui.moveTo(screen_x, screen_y, duration=0)
            # if right hand
            else:
                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                thumb_x, thumb_y = int(thumb_tip.x * frame_width), int(thumb_tip.y * frame_height)
                index_x, index_y = int(index_tip.x * frame_width), int(index_tip.y * frame_height)
                middle_x, middle_y = int(middle_tip.x * frame_width), int(middle_tip.y * frame_height)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (index_x, index_y), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(frame, (middle_x, middle_y), 10, (255, 0, 122), cv2.FILLED)
                # pinch distance calculation
                distanceRight = math.hypot(index_x - thumb_x, index_y - thumb_y)
                # if middle finger is close to index
                dragCheck = math.hypot(middle_x - index_x, middle_y - index_y)
                # fsm states, for dragging
                if drag_state == "IDLE":
                    if distanceRight < GESTURE_DISTANCE_THRESHOLD:
                        line_color = (0, 255, 0)
                        # checking for click lock
                        if not click_lock:
                            if dragCheck < GESTURE_DISTANCE_THRESHOLD:
                                pyautogui.mouseDown()
                                # change state to dragging
                                drag_state = "DRAGGING"
                                print("DRAG START")
                                cv2.putText(frame, "DRAGGING", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                            else:
                                # click if not dragging
                                pyautogui.click()
                                print(f"CLICK! (Distance: {distanceRight:.2f})")
                                # lock to prevent multiple clicks
                                click_lock = True
                                cv2.putText(frame, "CLICK!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, line_color, 3)

                    else:
                        # unlock the click for the next time user pinches
                        click_lock = False
                elif drag_state == "DRAGGING":
                    # if currently dragging, check for pinch release
                    if distanceRight >= GESTURE_DISTANCE_THRESHOLD:
                        pyautogui.mouseUp()
                        # change state back to idle
                        drag_state = "IDLE"
                        print("DRAG END")
            landmark = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            text_x = int(landmark.x * frame_width)
            text_y = int(landmark.y * frame_height)

            # drawing the hand label near the hand
            cv2.putText(
                img=frame,
                text=hand_label,
                org=(text_x - 30, text_y - 50),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1,
                color=(255, 0, 255),
                thickness=3
            )

    # frame display
    cv2.imshow('Click Gesture Tracker', frame)
    cv2.setWindowProperty('Click Gesture Tracker', cv2.WND_PROP_TOPMOST, cv2.WINDOW_KEEPRATIO) 

    # press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# clean resources
print("Closing resources.")
hands.close()
cap.release()
cv2.destroyAllWindows()