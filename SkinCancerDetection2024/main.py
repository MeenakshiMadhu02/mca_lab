import streamlit as st
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import cv2
import base64
import os

# Streamlit app configuration (must be the first Streamlit command)
st.set_page_config(page_title="Skin Cancer Detection", layout="wide")

# Load the trained model
model = load_model('skin_model.keras')

def set_background(jpg_file):
    """ Set the background image of the app. """
    with open(jpg_file, "rb") as f:
        bin_str = base64.b64encode(f.read()).decode()  # Encode image to base64
    # Adjusting MIME type to 'jpeg' if it's a JPEG image
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Add transparency to the sidebar
st.markdown("""
    <style>
        /* Apply transparency to the sidebar */
        section[data-testid="stSidebar"] {
            background-color: rgba(255, 255, 255, 0.3);  /* White background with 80% opacity */
        }
    </style>
    """, unsafe_allow_html=True)

# Set the background image from the desktop
desktop_image_path = os.path.expanduser("imgs.JPG")  # Update with your correct image path
set_background(desktop_image_path)

def preprocess_image(image):
    image = cv2.resize(image, (64, 64))  # Resize to (64, 64)
    image = np.array(image) / 255.0  # Normalize the image
    return np.expand_dims(image, axis=0)

# Sidebar

st.sidebar.title("Navigation")
st.sidebar.markdown("### About the App")
st.sidebar.markdown("This application uses a CNN model to detect skin cancer from uploaded images.")
st.sidebar.markdown("### How to Use")
st.sidebar.markdown("1. Upload an image of a skin lesion.")
st.sidebar.markdown("2. Click the 'Predict' button to see the results.")
st.sidebar.markdown("3. The model will indicate if the lesion is benign or malignant.")

# Header
st.markdown("<h1 style='text-align: center; color: #eb9515;'>🎗️ SKIN CANCER DETECTION 🎗️</h1>", unsafe_allow_html=True)

# Main content area
st.markdown("<div style='padding: 5px; border-radius: 10px; background-color: #e6edec;'>", unsafe_allow_html=True)

st.header("Upload an Image")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=400)

    if st.button('Predict'):
        img_array = np.array(image)
        preprocessed_image = preprocess_image(img_array)
        prediction = model.predict(preprocessed_image)

        if prediction[0][0] > 0.5:
            st.markdown("<h2 style='color: #dc3545;'>The model predicts: Malignant 🚨</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color: #28a745;'>The model predicts: Benign ✅</h2>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<footer style='text-align: center; margin-top: 20px;'><small>This application is for educational purposes only. Consult a healthcare professional for medical advice.</small></footer>", unsafe_allow_html=True)
