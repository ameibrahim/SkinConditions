from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
from PIL import Image
import requests
from io import BytesIO

application = Flask(__name__)

@application.route('/predict', methods=['POST'])
async def get_results(
    imageName: str,
    modelInputFeatureSize: int,
    modelFilename: str,
    domain: str
):
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
    print(preprocessed_image.shape)

    prediction = model.predict(preprocessed_image)
    score = tf.nn.softmax(prediction[0])

    predicted_class = ''

    if np.max(score* 100)<40 :
        predicted_class = 'Could not be processed'
    else:
        class_labels = ['acne', 'chickenpox', 'monkeypox', 'non-skin', 'normal']
        predicted_class = class_labels[np.argmax(score)]
    return predicted_class

if __name__ == '__main__':
    application.run()