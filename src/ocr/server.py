from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import easyocr
import uvicorn
import io
from PIL import Image

app = FastAPI(title="EasyOCR Web Service")

# Load the EasyOCR reader once (in background at startup)
@app.on_event("startup")
def load_ocr_model():
    global reader
    # Initialize EasyOCR with English by default (add more languages if needed)
    reader = easyocr.Reader(['en'], gpu=True)
    print("✅ EasyOCR model loaded and ready for use.")

@app.post("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/compass-ocr")
async def compass_ocr_endpoint(file: UploadFile = File(...)):
    try:
        # Read the uploaded image into memory
        image_bytes = await file.read()
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)

        # Perform OCR
        allowlist = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        results = reader.readtext(image_bytes, allowlist=allowlist, detail=1)

        # Format results into JSON-friendly structure
        response = [
            {
                "bbox": [[int(item) for item in sublist] for sublist in result[0]],
                "text": result[1],
                "confidence": result[2]
            }
            for result in results
        ]
        return JSONResponse(content={"results": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr")
async def ocr_endpoint(file: UploadFile = File(...)):
    try:
        # Read the uploaded image into memory
        image_bytes = await file.read()
        image_stream = io.BytesIO(image_bytes)
        image = Image.open(image_stream)

        # Perform OCR
        results = reader.readtext(image_bytes, detail=1)

        # Format results into JSON-friendly structure
        response = [
            {
                "bbox": [[int(item) for item in sublist] for sublist in result[0]],
                "text": result[1],
                "confidence": result[2]
            }
            for result in results
        ]
        return JSONResponse(content={"results": response})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server (localhost:8000 by default)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
