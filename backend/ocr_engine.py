import os
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

image_path = os.path.join(
    BASE_DIR,
    "reports_images",
    "clean",
    "P001_Month_1.png"
)

print("Exists:", os.path.exists(image_path))
print("Path:", image_path)

img = Image.open(image_path)

text = pytesseract.image_to_string(img)

print(text)