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
st.markdown("Convert any image into pixel art with optional animated styles.")

st.markdown("**Tip:** Drag and drop images to upload. Right-click > 'Copy Image' isn't supported yet.")

# Input method
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

pixel_size = st.slider("Pixelation Level", 10, 200, 80)
anim_style = st.selectbox("Animation Style", ["None", "Shimmer", "Glitch"])

# Pixelation & Animation
if image:
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    small = image.resize((pixel_size, pixel_size), Image.NEAREST)

    if anim_style == "None":
        pixel_art = small.resize(image.size, Image.NEAREST)
        st.subheader("🎨 Pixel Art Output")
        st.image(pixel_art, use_container_width=True)

        path = "pixel_art_output.png"
        pixel_art.save(path)
        with open(path, "rb") as f:
            st.download_button("Download Pixel Art (PNG)", f, file_name="pixel_art.png", mime="image/png")

    else:
        st.subheader("🎞️ Animated Pixel Art: " + anim_style)
        frames = []
        for i in range(6):
            noisy = np.array(small).copy()

            if anim_style == "Shimmer":
                noise = np.random.randint(-5, 5, noisy.shape, dtype=np.int8)
                noisy = np.clip(noisy + noise, 0, 255)

            elif anim_style == "Glitch":
                if i % 2 == 0:
                    noisy[:, :, 0] = np.roll(noisy[:, :, 0], 1, axis=1)  # Shift red
                else:
                    noisy[:, :, 1] = np.roll(noisy[:, :, 1], -1, axis=0)  # Shift green
                scanline = (np.random.rand(*noisy.shape[:2]) > 0.98).astype(np.uint8) * 255
                noisy[:, :, 2] = np.clip(noisy[:, :, 2] + scanline, 0, 255)  # Blue channel blink

            frame = Image.fromarray(noisy.astype(np.uint8)).resize(image.size, Image.NEAREST)
            frames.append(frame)

        gif_path = "animated_pixel_art.gif"
        imageio.mimsave(gif_path, frames, duration=0.15, loop=0)
        st.image(gif_path)

        with open(gif_path, "rb") as f:
            st.download_button("Download Animated GIF", f, file_name="pixel_art.gif", mime="image/gif")

