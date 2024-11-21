import tensorflow as tf
from tensorflow.keras.models import load_model
import streamlit as st
import numpy as np
from PIL import Image

st.header('Image Classification Model')

model = load_model(r'/Users/alhussein/Desktop/tf_CNN/Image_classify_final2.keras')

data_cat = ['acne', 'chickenpox', 'monkeypox', 'non-skin' ,'normal']

img_height = 180
img_width = 180

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", width=200)

    image = Image.open(uploaded_file)
    
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize((img_height, img_width))
    
    img_arr = tf.keras.preprocessing.image.img_to_array(image)
    
    img_bat = tf.expand_dims(img_arr, 0)
    
    predict = model.predict(img_bat)
    
    score = tf.nn.softmax(predict[0])
    
    if np.max(score* 100)<40 :
        st.write(f'Could not be processed')
    else :
        st.write(f'Skin Image in image is: {data_cat[np.argmax(score)]}')
