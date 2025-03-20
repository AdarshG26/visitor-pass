import pytesseract
from PIL import Image
import cv2
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def convert_image_to_text(image_path):
    # Read the image using OpenCV
    img = cv2.imread(image_path)

    # Check if the image is loaded correctly
    if img is None:
        raise ValueError(f"Error: Image not found at path {image_path}")
    
    # Convert the image to grayscale (optional, but often helps OCR accuracy)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text from the imagesaxs
    extracted_text = pytesseract.image_to_string(gray_img)
    print(extracted_text)
    return extracted_text

img_path = (r"static/css/imgs/pan.jpg")  # Replace with your image path


# Check if file exists before processing
if os.path.exists(img_path):
    text = convert_image_to_text(img_path)
    print("Extracted Text:\n", text)
else:
    print(f"Error: File {img_path} does not exist.")

