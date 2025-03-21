import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
import requests
import io
import imageio

st.set_page_config(page_title="Pixel Art Animator", layout="wide")
st.title("🎨 Pixelator")
st.markdown("Upload an image, select parts, and animate them with custom effects.")

# Sidebar for controls
st.sidebar.header("⚙️ Animation Controls")
option = st.sidebar.radio("Choose input method:", ("Upload Image", "Paste URL"))
image = None

if option == "Upload Image":
    uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
elif option == "Paste URL":
    url = st.sidebar.text_input("Enter image URL")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except:
            st.sidebar.error("Could not load the image from URL.")

# Animation Settings
pixel_size = st.sidebar.slider("Pixelation Level", 10, 200, 80)
frame_count = st.sidebar.slider("Number of Frames", 2, 8, 4, step=2)
fps = st.sidebar.slider("Animation Speed (FPS)", 5, 30, 12)
anim_type = st.sidebar.selectbox("Animation Style", ["None", "Blinking", "Bobbing", "Glitch", "Colour Shift"])
color_shift_intensity = st.sidebar.slider("Colour Shift Intensity", 0, 20, 5)
highlight_area = st.sidebar.checkbox("Manually Select Animation Area", value=False)

if image:
    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    small = image.resize((pixel_size, pixel_size), Image.NEAREST)
    image_size = image.size

    if highlight_area:
        st.sidebar.warning("⚠️ Click & drag on the image to select the animated area (coming soon)")
        # Placeholder for selection feature

    if anim_type == "None":
        pixel_art = small.resize(image_size, Image.NEAREST)
        st.subheader("🎨 Static Pixel Art")
        st.image(pixel_art, use_container_width=True)

        output_path = "pixel_art.png"
        pixel_art.save(output_path)
        with open(output_path, "rb") as f:
            st.download_button("Download Pixel Art (PNG)", f, file_name="pixel_art.png", mime="image/png")

    else:
        st.subheader("🎞️ Animated Pixel Art")
        frames = []
        for i in range(frame_count):
            modified = np.array(small)

            if anim_type == "Blinking":
                if i % 2 == 0:
                    modified[:, :, 0] = 0  # Black out the red channel on every other frame
            
            elif anim_type == "Bobbing":
                shift = (i % 2) * 2 - 1  # Move up/down
                modified = np.roll(modified, shift, axis=0)

            elif anim_type == "Glitch":
                if i % 2 == 0:
                    modified[:, :, 0] = np.roll(modified[:, :, 0], 1, axis=1)  # Shift red
                else:
                    modified[:, :, 1] = np.roll(modified[:, :, 1], -1, axis=0)  # Shift green
                scanline = (np.random.rand(*modified.shape[:2]) > 0.98).astype(np.uint8) * 255
                modified[:, :, 2] = np.clip(modified[:, :, 2] + scanline, 0, 255)

            elif anim_type == "Colour Shift":
                modified = modified.astype(np.float32)
                modified += np.sin(i * 2 * np.pi / frame_count) * color_shift_intensity
                modified = np.clip(modified, 0, 255).astype(np.uint8)

            frame = Image.fromarray(modified).resize(image_size, Image.NEAREST)
            frames.append(frame)

        gif_path = "animated_pixel_art.gif"
        imageio.mimsave(gif_path, frames, duration=1/fps, loop=0)
        st.image(gif_path)

        with open(gif_path, "rb") as f:
            st.download_button("Download Animated GIF", f, file_name="pixel_art.gif", mime="image/gif")
