import cv2
import numpy as np
from skimage.feature import local_binary_pattern
import joblib
from flask_cors import CORS
import requests
from io import BytesIO
from flask import Flask, request, jsonify
from PIL import Image

def extract_lbp_features(image, P=8, R=1):
    """
    Extract Local Binary Patterns (LBP) features from an image.
    :param image: Input grayscale image.
    :param P: Number of circularly placed pixels.
    :param R: Radius of the circle.
    :return: LBP feature vector.
    """
    lbp = local_binary_pattern(image, P, R, method='uniform')
    (hist, _) = np.histogram(lbp.ravel(), bins=np.arange(0, P + 3), range=(0, P + 2))
    hist = hist.astype('float')
    hist /= (hist.sum() + 1e-6)  # Normalize histogram
    return hist

def predict_single_image(image, model, class_names):
    """
    Predict the class of a single image using the trained classifier.
    :param image: PIL Image object.
    :param model: A tuple containing the trained classifier and scaler.
    :param class_names: List of class names.
    :return: Predicted class name.
    """
    classifier, scaler = model

    # Convert PIL Image to a grayscale numpy array
    image = image.convert('L')
    image_np = np.array(image)

    # Extract LBP features
    lbp_features = extract_lbp_features(image_np)
    lbp_features = scaler.transform([lbp_features])  # Scale features

    # Predict the class
    prediction = classifier.predict(lbp_features)
    print(prediction)
    predicted_class = class_names[prediction[0]]
    
    return predicted_class

# Load the model (classifier and scaler)
model = joblib.load("../models/model.pkl")
class_names = ['acne', 'chickenpox', 'normal', 'monkeypox']

application = Flask(__name__)
CORS(application)

@application.route("/predict/", methods=['GET'])
def get_results():

    image_name = request.args.get("imageName")
    size = request.args.get("modelInputFeatureSize")
    model_name = request.args.get("modelFilename")
    domain = request.args.get("domain")

    print(domain)
    print("size: ", size)

    size = int(size)

    url = f"http://{domain}/uploads/" + image_name
    
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))

    model_name = "../models/" + model_name

    result = predict_single_image(image, model, class_names)

    results = {
        "classification": result
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()