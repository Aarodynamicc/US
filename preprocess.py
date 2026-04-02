import cv2
import numpy as np

def preprocess_image(img, size=300):
    img = cv2.resize(img, (size, size))
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img