import os
import logging
import base64
from io import BytesIO

import numpy as np
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Set up logging with DEBUG level for detailed logs
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("prediction_api")

def preprocess_image(img: Image.Image, size: int) -> np.ndarray:
    logger.debug("Starting image preprocessing...")
    img = img.convert("RGB")
    logger.debug("Converted image to RGB")
    img = img.resize((size, size), Image.Resampling.LANCZOS)
    logger.debug(f"Resized image to {size}x{size}")
    img_array = image.img_to_array(img, dtype=np.uint8)
    logger.debug("Converted image to array")
    img_array = img_array / 255.0
    logger.debug("Normalized image array")
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    logger.debug(f"Final preprocessed image shape: {img_array.shape}")
    return img_array

def predict_image(model, img: Image.Image, size: int) -> dict:
    logger.debug("Predicting image...")
    labels = {0: 'acne', 1: 'chickenpox', 2: 'monkeypox', 3: 'non-skin', 4: 'normal'}
    preprocessed_img = preprocess_image(img, size)
    logger.debug(f"Model input shape: {preprocessed_img.shape}")

    # Validate image shape
    expected_shape = (1, size, size, 3)
    if preprocessed_img.shape != expected_shape:
        error_msg = f"Unexpected image shape: {preprocessed_img.shape}, expected: {expected_shape}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    # Get main prediction
    prediction = model.predict(preprocessed_img)
    logger.debug(f"Raw prediction output: {prediction}")

    max_prob = float(np.max(prediction[0]))
    predicted_class_index = int(np.argmax(prediction[0]))
    predicted_class = labels.get(predicted_class_index, "Unknown")
    classes_probabilities = {labels[i]: float(round(prob * 100, 2))
                              for i, prob in enumerate(prediction[0])}

    # If predicted class is monkeypox, predict stage using the same model's stages logic.
    # (Adjust this as needed. In this example, we assume "stages.keras" handles stage prediction.)
    predicted_stage = "stage_0"
    if predicted_class == 'monkeypox':
        # Re-load the stages model (if needed) or perform any extra prediction steps.
        stages_model_path = '/app/models/stages.keras'
        logger.debug(f"Loading stages model from: {stages_model_path}")
        stages_model = load_model(stages_model_path)
        logger.debug(f"Stages model input shape: {stages_model.input_shape}")
        labels_stages = {0: 'stage_1', 1: 'stage_2', 2: 'stage_3', 3: 'stage_4'}
        stage_prediction = stages_model.predict(preprocessed_img)
        logger.debug(f"Stages raw prediction output: {stage_prediction}")
        predicted_stage_index = int(np.argmax(stage_prediction[0]))
        predicted_stage = labels_stages.get(predicted_stage_index, "Unknown")

    result = {
        "max_prob": max_prob,
        "predicted_class": predicted_class,
        "class_probabilities": classes_probabilities,
        "predicted_stage": predicted_stage
    }
    logger.debug(f"Final prediction result: {result}")
    return result

def predict_with_image(img: Image.Image, model_filename: str, size: int) -> dict:
    model_path = f"/app/models/{model_filename}"
    logger.info(f"Loading model from: {model_path}")
    try:
        model = load_model(model_path)
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise
    return predict_image(model, img, size)

# Create FastAPI application instance
app = FastAPI()
logger.debug("Created FastAPI application")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.debug("Configured CORS middleware")

# ------------------------------------------------------------------------------
# Single endpoint for base64 image prediction.
# This endpoint always uses the "stages.keras" model.
# ------------------------------------------------------------------------------
@app.post("/predict_base64/")
async def predict_base64_endpoint(
    image_base64: str = Body(..., embed=True),
    modelInputFeatureSize: int = Body(..., embed=True)
):
    try:
        logger.info("Decoding base64 image from request")
        image_data = base64.b64decode(image_base64)
        img = Image.open(BytesIO(image_data))
        logger.info("Loaded image from base64 successfully")
        # Always use 'stages.keras' for prediction
        prediction_result = predict_with_image(img, "stages.keras", modelInputFeatureSize)
        logger.info(f"Prediction result: {prediction_result}")
        return {"classification": prediction_result}
    except Exception as e:
        logger.error(f"Error in /predict_base64/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    
    # ------------------------------------------------------------------------------
@application.get("/predict/")
async def predict_endpoint(
    imageName: str,
    modelInputFeatureSize: int,
    modelFilename: str,
    domain: str
):
    try:
        image_url = f"http://{domain}/uploads/{imageName}"
        logger.info(f"Fetching image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()
        content_type = response.headers.get('Content-Type')
        logger.info(f"Image response status: {response.status_code}, Content-Type: {content_type}")
        
        if content_type not in ['image/jpeg', 'image/png', 'image/svg+xml']:
            error_msg = "Received content is not a valid image."
            logger.error(error_msg)
            raise HTTPException(status_code=400, detail=error_msg)

        if content_type == 'image/svg+xml':
            import cairosvg
            png_data = cairosvg.svg2png(bytestring=response.content)
            img = Image.open(BytesIO(png_data))
            logger.info("Converted SVG image to PNG")
        else:
            img = Image.open(BytesIO(response.content))
            logger.info("Loaded image successfully")

        prediction_result = predict_with_image(img, modelFilename, modelInputFeatureSize)
        logger.info(f"Prediction result: {prediction_result}")
        return {"classification": prediction_result}
    
    except Exception as e:
        logger.error(f"Error in /predict/ endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
#------------------------------------------------------------
@application.get("/test-model-access/")
async def test_model_access():
    model_path = "/app/models/stages.keras"
    if os.path.exists(model_path):
        logger.info(f"Model file found: {model_path}")
        return JSONResponse(content={"status": "success", "message": "Model file is accessible."})
    else:
        logger.error(f"Model file not found: {model_path}")
        return JSONResponse(content={"status": "error", "message": "Model file is not accessible."})
#------------------------------------------------------------
@application.get("/list-models/")
async def list_models():
    models_path = "/app/models"
    if os.path.exists(models_path):
        files = os.listdir(models_path)
        logger.info(f"Models in directory {models_path}: {files}")
        return JSONResponse(content={"status": "success", "files": files})
    else:
        logger.error(f"Models directory not accessible: {models_path}")
        return JSONResponse(content={"status": "error", "message": "Models directory is not accessible."})
    

    
if __name__ == "__main__":
    import uvicorn
    logger.info("Starting server on 0.0.0.0:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)
