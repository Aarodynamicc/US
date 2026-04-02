import sys
import os
import time
from collections import deque, Counter
import json

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import cv2
import numpy as np
from tensorflow.keras.models import load_model

from utils.hand_tracker import HandTracker
from utils.preprocess import preprocess_image
from utils.speech import speak

# Load model and labels
model = load_model("model/sign_model.h5")
with open("model/labels.json") as f:
    class_indices = json.load(f)
labels = list(class_indices.keys())

tracker = HandTracker()

# Camera Setup for WSL
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

pred_queue = deque(maxlen=10)
last_spoken = ""
last_speech_time = 0
window_name = "Sign Language Detection"

print("Starting Detection... Press 'q' or ESC to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret: break
            
        frame = cv2.flip(frame, 1) # Mirror
        bbox = tracker.get_hand_bbox(frame)

        if bbox:
            x1, y1, x2, y2 = bbox
            hand = frame[y1:y2, x1:x2]

            if hand.size != 0:
                img = preprocess_image(hand)
                pred = model.predict(img, verbose=0)
                label = labels[np.argmax(pred)]
                pred_queue.append(label)

                if len(pred_queue) == 10:
                    counts = Counter(pred_queue).most_common(1)
                    if counts:
                        
                        letter = str(counts[0][0])
                        
                        current_time = time.time()
                        if letter != last_spoken and (current_time - last_speech_time) > 2:
                            sys.stdout.write(f"\rPrediction: {letter}\n")
                            sys.stdout.flush()
                            speak(letter)
                            last_spoken = letter
                            last_speech_time = current_time

                cv2.putText(frame, f"Sign: {label}", (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
        else:
            cv2.putText(frame, "No Hand Detected", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

        cv2.imshow(window_name, frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27 or cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    os._exit(0)
