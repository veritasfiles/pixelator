# streamlit_app.py

import streamlit as st
from PIL import Image
import requests
import io

st.set_page_config(page_title="Pixel Art Generator", layout="centered")
st.title("🎨 Pixel Art Generator")
st.markdown("Convert any image into pixel art while preserving the original aesthetic.")

# User input method
option = st.radio("Choose an input method:", ("Upload an image", "Paste an image URL"))

image = None

if option == "Upload an image":
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

elif option == "Paste an image URL":
    url = st.text_input("Enter the image URL")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except:
            st.error("Could not load image from URL.")

# Pixel size slider
pixel_size = st.slider("Pixelation Level (higher = more detail)", min_value=10, max_value=200, value=80)

# Generate and show pixel art
if image:
    st.subheader("Original Image")
    st.image(image, use_column_width=True)

    # Resize and pixelate
    small = image.resize((pixel_size, pixel_size), Image.NEAREST)
    pixel_art = small.resize(image.size, Image.NEAREST)

    st.subheader("🟡 Pixel Art Output")
    st.image(pixel_art, use_column_width=True)

    # Download button
    output_path = "pixel_art_output.png"
    pixel_art.save(output_path)
    with open(output_path, "rb") as f:
        st.download_button("Download Pixel Art", f, file_name="pixel_art_output.png", mime="image/png")
