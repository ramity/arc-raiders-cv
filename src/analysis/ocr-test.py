import cv2
import requests

# URL of the OCR endpoint
OCR_URL = "http://arc_raiders_ocr:8000/ocr"

# Load an image using OpenCV (can also be a frame from video capture)
image = cv2.imread("roi.jpg")

# Encode the image as JPEG in memory
_, img_encoded = cv2.imencode('.jpg', image)

# Send it to the OCR API
files = {"file": ("frame.jpg", img_encoded.tobytes(), "image/jpeg")}
response = requests.post(OCR_URL, files=files)

# Parse the JSON response
if response.status_code == 200:
    data = response.json()
    print("✅ OCR Results:")
    print(data)
    for item in data["results"]:
        print(f"Text: {item['text']} (conf: {item['confidence']:.2f})")
else:
    print("❌ Error:", response.text)
