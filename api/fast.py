from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
from PIL import Image
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from io import BytesIO
import logging
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set to DEBUG for more verbosity
logger = logging.getLogger(__name__)

def preprocess_image(_image, size):
    _image = _image.convert("RGB")
    img = _image.resize((size, size), Image.Resampling.LANCZOS)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predictWithImage(_image, model_name, size):
    loaded_model = load_model(model_name)
    return predict_image(loaded_model, _image, size)

def predict_image(model, _image, size):
    preprocessed_image = preprocess_image(_image, size)
    logger.info(f"Preprocessed image shape: {preprocessed_image.shape}")

    prediction = model.predict(preprocessed_image)
    score = tf.nn.softmax(prediction[0])

    predicted_class = ''

    if np.max(score * 100) < 40:
        predicted_class = 'Could not be processed'
    else:
        class_labels = ['acne', 'chickenpox', 'monkeypox', 'non-skin', 'normal']
        predicted_class = class_labels[np.argmax(score)]
    return predicted_class

# Create FastAPI instance
application = FastAPI()

# Set up CORS
application.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your domain here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging Middleware
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

application.add_middleware(LoggingMiddleware)

@application.get("/predict/")
async def get_results(
    imageName: str,
    modelInputFeatureSize: int,
    modelFilename: str,
    domain: str
):
    try:
        url = f"https://{domain}/uploads/{imageName}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        img = Image.open(BytesIO(response.content))

        model_name = "../models/" + modelFilename
        result = predictWithImage(img, model_name, modelInputFeatureSize)

        results = {
            "classification": result,
        }

        return results

    except Exception as e:
        logger.error(f"Error occurred while processing: {str(e)}")  # Log the error
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(application, host="0.0.0.0", port=8001)
