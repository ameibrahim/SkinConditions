import os
import numpy as np
import cv2
import tensorflow as tf
import streamlit as st

# Load the model
model = 'cnnmodel.keras'
model = tf.keras.models.load_model(model)

# Preprocess the image
def preprocess_image(image):
    img = cv2.resize(image, (128, 128))  # Resize to the same size as used in training
    img = img / 255.0  # Normalize pixel values to [0, 1]
    return img

# Define class labels
class_labels = ['cancer', 'chickenpox', "cowpox", "healthy", "measles", "monkeypox"]

# Streamlit interface
st.title("Skin Condition Predictor")
st.write("This application predicts if you have diseases such as chickenpox, measles, cowpox or monkeypox.")
st.write("Upload an image to classify if you are sick.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join('uploads', uploaded_file.name)
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Read the image using OpenCV
    image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
    
    # Preprocess the image
    preprocessed_img = preprocess_image(image)
    preprocessed_img = np.expand_dims(preprocessed_img, axis=0)  # Add batch dimension
    
    # Make prediction
    prediction = model.predict(preprocessed_img)
    predicted_label = np.argmax(prediction)
    predicted_class_name = class_labels[predicted_label]
    
    st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
    st.title(f"Prediction: {predicted_class_name}")