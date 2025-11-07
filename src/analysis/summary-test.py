import cv2
import requests

ARTICLE = """
A model input example provides a concrete, valid instance of the data format a machine learning model expects to receive. Summarizing this involves creating a concise, clear description or representation of the required input structure, type, and constraints for documentation and validation purposes. 
Purpose of Summarizing the Input Example

    Documentation: Serves as a clear, living document for developers and users on how to interact with the model.
    Validation: Allows tools (like MLflow deployment systems) to automatically check if new data conforms to the expected format, catching errors early.
    Usability: Helps users understand the required data format at a glance, without needing to delve into the model's internal workings.
    Consistency: Ensures all interactions with the model follow a consistent data format, leading to more reliable performance. 

Key Components of a Summarized Input Example
A summarized model input example should clearly define:

    Data Type: The expected type (e.g., integer, string, float, boolean, dictionary, Pandas DataFrame, or tensor).
    Shape/Dimensions: For structured data or arrays, the required dimensions (e.g., an image might be a 3D tensor of shape (height, width, channels)).
    Features/Columns: The specific input variables or features the model uses (e.g., square footage, age, number of bedrooms for a house price model).
    Constraints: Any limitations on the values, such as ranges, allowed categories, or maximum length (e.g., text input max length of 512 tokens).
    Format: The specific data serialization format, if applicable (e.g., JSON, CSV, etc.).
"""

# URL of the OCR endpoint
OCR_URL = "http://arc_raiders_summary:8000/summarize"

# Send it to the OCR API
response = requests.post(OCR_URL, data=ARTICLE)

# Parse the JSON response
if response.status_code == 200:
    data = response.json()
    print("✅ Summary Results:")
    print(data)
else:
    print("❌ Error:", response.text)
