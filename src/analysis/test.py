import cv2
import pytesseract
import os
import numpy
import requests
import time

# Config
OCR_URL = "http://arc_raiders_ocr:8000/ocr"
VIDEO_DIR = "/root/videos"
VIDEO_FILE = "2608011038.mp4"
VIDEO_PATH = os.path.join(VIDEO_DIR, VIDEO_FILE)
# START_FRAME_NUMBER = 22517
START_FRAME_NUMBER = (8*60*60)+(37.5*60)
FRAME_COUNT = 1

COMPASS_BEARING_VALUE_SUBREGION = (942, 16, 36, 24)
COMPASS_TEXT_SUBREGION = (783, 73, 371, 26)
MATCH_TIMER_SUBREGION = (930, 100, 60, 24)
RETURN_POINT_SHUTDOWN_NOTICE_REGION = (712, 184, 503, 88)

FRAME_RATE_COUNTER_SUBREGION = (1866, 0, 54, 21)

LOCATION_TEXT_SUBREGION = (22, 389, 392, 87)

XP_LOGS_SUBREGION = (23, 308, 355, 118)

PLAYER_PROXIMITY_VOICE_SUBREGION = (21, 592, 288, 39)

PLAYER_2_BOUNDING_BOX = (39, 876, 271, 68)
PLAYER_2_COLOR_SUBREGION = (45, 895, 6, 20)

PLAYER_1_BOUNDING_BOX = (40, 944, 270, 90)

PLAYER_1_ARMOR_NW_POINT = (40, 994)
PLAYER_1_ARMOR_NE_POINT = (309, 966)
PLAYER_1_ARMOR_SE_POINT = (309, 981)
PLAYER_1_ARMOR_SW_POINT = (40, 1011)
PLAYER_1_ARMOR_BOUNDING_BOX = (40, 966, 269, 46)
# src_points = numpy.float32([PLAYER_1_ARMOR_NW_POINT, PLAYER_1_ARMOR_NE_POINT, PLAYER_1_ARMOR_SW_POINT, PLAYER_1_ARMOR_SE_POINT]) 
# dst_points = numpy.float32([[0, 0], [w, 0], [0, h], [w, h]])
# M = cv2.getPerspectiveTransform(src_points, dst_points)
# unwarped_image = cv2.warpPerspective(frame, M, (w, h))

PLAYER_1_HEALTH_NW_POINT = (40, 1016)
PLAYER_1_HEALTH_NE_POINT = (309, 986)
PLAYER_1_HEALTH_SE_POINT = (309, 1001)
PLAYER_1_HEALTH_SW_POINT = (40, 1033)
PLAYER_1_HEALTH_BOUNDING_BOX = (40, 986, 269, 46)
# src_points = numpy.float32([PLAYER_1_HEALTH_NW_POINT, PLAYER_1_HEALTH_NE_POINT, PLAYER_1_HEALTH_SW_POINT, PLAYER_1_HEALTH_SE_POINT]) 
# dst_points = numpy.float32([[0, 0], [w, 0], [0, h], [w, h]])
# M = cv2.getPerspectiveTransform(src_points, dst_points)
# unwarped_image = cv2.warpPerspective(frame, M, (w, h))

STAMINA_BAR_SUBREGION = (857, 968, 206, 16)

PATCH_SERVER_LOBBY_REGION = (1731, 1060, 160, 20)

RELOAD_INDICATOR_SUBREGION = (940, 520, 40, 40)

QUICK_ITEM_1_SUBREGION = (1536, 909, 64, 92)
QUICK_ITEM_2_SUBREGION = (1608, 914, 64, 94)

UNSELECTED_SECONDARY_WEAPON_BOUNDING_BOX = (1680, 980, 200, 55)
SELECTED_PRIMARY_WEAPON_BOUNDING_BOX = (1680, 883, 200, 112)
SELECTED_PRIMARY_WEAPON_CURRENT_AMMO_SUBREGION = (1698, 924, 53, 28)
SELECTED_PRIMARY_WEAPON_RESERVE_AMMO_SUBREGION = (1720, 952, 32, 17)

FLASHLIGHT_TOOL_TIP_REGION = (1743, 821, 140, 37)
UNARMED_TOOL_TIP_REGION = (1743, 784, 140, 37)

# Old tesseract stuff

# SUBREGION = (700, 16, 550, 24) # compass
# SUBREGION = (936, 16, 48, 24) # bearing
# SUBREGION = (942, 16, 36, 24) # subregion within bearing
# custom_config = r'--oem 3 --psm 8 outputbase digits'
# custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=NESW'
# compass_array = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]

# Open video file and navigate to desired start frame
capture = cv2.VideoCapture(VIDEO_PATH)

if not capture.isOpened():
    raise FileNotFoundError(f"Could not open video file: {video_path}")

# Set the frame position
capture.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME_NUMBER)

results = []

for offset in range(FRAME_COUNT):
    ret, frame = capture.read()
    if not ret:
        raise ValueError(f"Could not read frame {START_FRAME_NUMBER} from video.")
    cv2.imwrite("frame.jpg", frame)

    # Extract region of interest (ROI)
    x, y, w, h = FLASHLIGHT_TOOL_TIP_REGION
    roi = frame[y:y + h, x:x + w]
    cv2.imwrite("roi.jpg", roi)

    _, img_encoded = cv2.imencode('.jpg', roi)

    # Send it to the OCR API
    files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
    response = requests.post(OCR_URL, files=files)

    # Parse the JSON response
    if response.status_code == 200:
        data = response.json()
        # results.append(data["results"])
        for item in data["results"]:
            results.append(item["text"])
    else:
        print("❌ Error:", response.text)
    
    print(START_FRAME_NUMBER + offset)
    time.sleep(0.5)

capture.release()
print(results)


# Preprocess ROI for OCR
# gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_TOZERO_INV)
# threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 3, 10)

# 2x scale
# scaled = cv2.resize(gray, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)
# cv2.imwrite("scaled.jpg", scaled)

# result = reader.readtext(scaled)
# print(result)

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


