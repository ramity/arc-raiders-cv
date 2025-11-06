import cv2
import pytesseract
import os
import numpy
import easyocr

# Config
VIDEO_DIR = "/root/videos"
FRAME_NUMBER = 56005
# SUBREGION = (700, 16, 550, 24) # compass
# SUBREGION = (936, 16, 48, 24) # bearing
SUBREGION = (942, 16, 36, 24) # subregion within bearing
# custom_config = r'--oem 3 --psm 8 outputbase digits'
# custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=NESW'
# compass_array = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Init easyocr
reader = easyocr.Reader(['en'], gpu=False)

filename = "2608011038.mp4"
video_path = os.path.join(VIDEO_DIR, filename)
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    raise FileNotFoundError(f"Could not open video file: {video_path}")

# Set the frame position
cap.set(cv2.CAP_PROP_POS_FRAMES, FRAME_NUMBER)
ret, frame = cap.read()
if not ret:
    raise ValueError(f"Could not read frame {FRAME_NUMBER} from video.")
cv2.imwrite("frame.jpg", frame)

# Extract region of interest (ROI)
x, y, w, h = SUBREGION
roi = frame[y:y + h, x:x + w]
cv2.imwrite("roi.jpg", roi)

# Preprocess ROI for OCR
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_TOZERO_INV)
# threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 10)

# 2x scale
scaled = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
cv2.imwrite("scaled.jpg", scaled)

result = reader.readtext(scaled)
print(result)

# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# gray = clahe.apply(gray)

# OCR on the region
# text = pytesseract.image_to_string(threshold, config=custom_config)
# print(text)

# boxes = pytesseract.image_to_boxes(threshold, config=custom_config)
# for b in boxes.splitlines():
#     char, x1, y1, x2, y2, _ = b.split()
#     x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
#     cv2.rectangle(threshold, (x1, y1), (x2, y2), 0, 1)
#     cv2.putText(gray, char, (x1, y1 + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# print(pytesseract.image_to_data(threshold, config=custom_config))

# cv2.imwrite("boxed_characters.jpg", threshold)

cap.release()
