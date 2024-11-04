import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

loaded_best_model = load_model("model_10-0.92.keras")



labels = {0: 'acne', 1: 'chickenpox', 2: 'monkeypox', 3: 'non-skin', 4: 'normal'}

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    
    img = img.resize((300, 300))
    
    img_arr = image.img_to_array(img, dtype=np.uint8)
    
    img_arr = img_arr / 255.0
    
    p = loaded_best_model.predict(img_arr[np.newaxis, ...])
    
    max_prob = np.max(p[0])
    predicted_class = labels[np.argmax(p[0])]
    
    st.write(f"Predicted Class: {predicted_class}")
    st.write(f"Maximum Probability: {max_prob:.2f}")

    st.write("\n### Individual Probabilities:")
    
    classes = []
    prob = []

    for i, j in enumerate(p[0]):
        class_name = labels[i]
        classes.append(class_name)
        prob.append(round(j * 100, 2))
        st.write(f"{class_name.upper()}: {round(j * 100, 2)}%")
    
    df = pd.DataFrame({'Classes': classes, 'Probabilities': prob})
    
    st.bar_chart(df.set_index('Classes')['Probabilities'], height=300)
