from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from io import BytesIO


def preprocess_image(_image, size):
    _image = _image.convert("RGB")
    img = _image.resize((size,size), Image.Resampling.LANCZOS)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array

def predictWithImage(_image, model_name, size):
    loaded_model = load_model(model_name)
    return predict_image(loaded_model, _image, size)

def predict_image(model, _image, size):
    preprocessed_image = preprocess_image(_image, size)
    print(preprocessed_image.shape)
    prediction = model.predict(preprocessed_image)
    class_index = np.argmax(prediction)
    class_labels = ['cancer', 'chickenpox', "cowpox", "healthy", "measles", "monkeypox"]
    predicted_class = class_labels[class_index]
    return predicted_class

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
    img = Image.open(BytesIO(response.content))

    model_name = "../models/" + model_name

    result = predictWithImage(img, model_name, size)

    results = {
        "classification": result,
    }

    response = jsonify(results)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
   application.run()