from rembg import remove
from PIL import Image, ImageOps
import cv2
import numpy as np
import sys
import os

def preprocess(image_path):
    image = Image.open(image_path).convert("RGBA")

    image = remove(image)

    image_np = np.array(image)

    alpha = image_np[:, :, 3]

    rgb = image_np[:, :, :3]

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    clahe = cv2.createCLAHE(
        clipLimit=2.5,
        tileGridSize=(8, 8)
    )

    gray = clahe.apply(gray)

    white = np.full_like(gray, 255)

    gray = np.where(alpha > 0, gray, white)

    result = Image.fromarray(gray)

    result = ImageOps.autocontrast(result)

    os.makedirs("images", exist_ok=True)

    output = "images/source-prepped.png"

    result.save(output)

    print(f"Saved: {output}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage:")
        print("python scripts/prep_photo.py images/omer.jpeg")
        sys.exit()

    preprocess(sys.argv[1])