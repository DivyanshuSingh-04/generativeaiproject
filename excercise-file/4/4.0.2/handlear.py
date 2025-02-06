import openai
from dotenv import load_dotenv
from PIL import Image
import requests
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Folder path for saving images
folder_path = "media"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)


def download_file(user_input, url):
    """Download a file from a URL and save it to the media folder"""
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()

        file_path = os.path.join(
            folder_path, os.path.basename("image_" + user_input.replace(" ", "_")) + ".png"
        )
        with open(file_path, "wb") as f:
            f.write(r.content)
        return f"File downloaded successfully at {file_path}"
    except requests.RequestException as e:
        return f"Error downloading file: {e}"


def get_files():
    """Get all image files in the folder"""
    files = os.listdir(folder_path)
    images = []
    image_files = [f for f in files if f.endswith(".jpg") or f.endswith(".png")]

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = Image.open(image_path)
        images.append({"file": image, "title": image_file})
    return images


def generate_images(user_input="a white cat"):
    """Generate an image using the OpenAI API"""
    response = openai.Image.create(
        prompt=user_input,
        size="256x256",
        n=1,
    )
    return response["data"][0]["url"]
