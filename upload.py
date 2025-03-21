# streamlit_app.py

import streamlit as st
from PIL import Image
import requests
import io
import numpy as np
import imageio
import os

st.set_page_config(page_title="Pixel Art Generator", layout="centered")
st.title("🟣 Pixel Art Generator")
st.markdown("Convert any image into pixel art — static or animated.")

st.markdown("**Tip:** You can drag and drop an image from your desktop or browser. Right-click > 'Copy Image' won't work yet due to Streamlit limitations.")

# Upload or URL
option = st.radio("Choose an input method:", ("Upload an image", "Paste an image URL"))

image = None
if option == "Upload an image":
    uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

elif option == "Paste an image URL":
    url = st.text_input("Paste an image URL:")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except:
            st.error("Could not load the image from the URL provided.")

# Pixelation level
pixel_size = st.slider("Pixelation Level (higher = more detail)", 10, 200, 80)

# Animation toggle
animate = st.checkbox("Add subtle animation (shimmer)")

# Display and Process
if image:
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    # Pixelation
    small = image.resize((pixel_size, pixel_size), Image.NEAREST)
    
    if not animate:
        pixel_art = small.resize(image.size, Image.NEAREST)
        st.subheader("🎨 Pixel Art Output")
        st.image(pixel_art, use_container_width=True)

        # Download static
        output_path = "pixel_art_output.png"
        pixel_art.save(output_path)
        with open(output_path, "rb") as f:
            st.download_button("Download Pixel Art", f, file_name="pixel_art_output.png", mime="image/png")

    else:
        st.subheader("✨ Animated Pixel Art")
        frames = []
        for _ in range(6):
            noise = np.random.randint(-5, 5, (small.size[1], small.size[0], 3), dtype=np.int8)
            noisy_frame = np.clip(np.array(small) + noise, 0, 255).astype(np.uint8)
            frame_img = Image.fromarray(noisy_frame).resize(image.size, Image.NEAREST)
            frames.append(frame_img)

        gif_path = "animated_pixel_art.gif"
        imageio.mimsave(gif_path, frames, duration=0.15)
        st.image(gif_path)

        # Download animated
        with open(gif_path, "rb") as f:
            st.download_button("Download Animated GIF", f, file_name="pixel_art.gif", mime="image/gif")
