# Pixel Art Generator for Google Colab
import requests
from PIL import Image
import io
import matplotlib.pyplot as plt
from google.colab import files

# Function to load image from URL or upload
def load_image():
    print("Choose an option:")
    print("1: Upload an image")
    print("2: Paste an image URL")
    choice = input("Enter 1 or 2: ")

    if choice == "1":
        uploaded = files.upload()
        filename = list(uploaded.keys())[0]
        image = Image.open(filename)
    elif choice == "2":
        url = input("Enter the image URL: ")
        response = requests.get(url)
        image = Image.open(io.BytesIO(response.content))
    else:
        print("Invalid choice. Restart and enter 1 or 2.")
        return None
    return image.convert("RGB")

# Function to generate pixel art
def generate_pixel_art(image, pixel_size=80):
    original_size = image.size
    small_img = image.resize((pixel_size, pixel_size), Image.NEAREST)
    pixel_art = small_img.resize(original_size, Image.NEAREST)
    return pixel_art

# Run the process
image = load_image()
if image:
    print("Generating pixel art...")
    pixel_art = generate_pixel_art(image, pixel_size=120)

    # Show pixel art
    plt.imshow(pixel_art)
    plt.axis("off")
    plt.show()

    # Save and download the result
    pixel_art_path = "pixel_art_output.png"
    pixel_art.save(pixel_art_path)
    files.download(pixel_art_path)

