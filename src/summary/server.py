from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from transformers import pipeline
import uvicorn
import io

app = FastAPI(title="facebook/bart-large-cnn summarization model")

# Load the EasyOCR reader once (in background at startup)
@app.on_event("startup")
def load_ocr_model():
    global summarizer
    # Initialize summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    print("✅ Summarization model loaded and ready for use.")

@app.post("/summarize")
async def summarize_endpoint(request: Request):
    try:
        # Read the raw body as bytes
        raw_body = await request.body()
        
        # Decode the bytes to a string (assuming UTF-8 encoding)
        text_content = raw_body.decode("utf-8")

        # Perform summarization
        results = summarizer(text_content, max_length=130, min_length=30, do_sample=False)

        # Format results into JSON-friendly structure
        return JSONResponse(content={"results": results})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Run the server (localhost:8000 by default)
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
