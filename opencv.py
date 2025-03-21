import pytesseract
from PIL import Image
import cv2
import os

def convert_image_to_text(pan):
    # Read the image using OpenCV
    img = cv2.imread(pan)
    print(f"print the type of img is :{type(img)}")
    exit

    # Check if the image is loaded correctly
    # The raise keyword is used to raise an exception. You can define what kind of error to raise, and the text to print to the user. 
    if img is None:
        raise ValueError(f"Error: Image not found at path {pan}")
    
    # Convert the image to grayscale (optional, but often helps OCR accuracy)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text from the imagesaxs
    text = pytesseract.image_to_string(gray_img)
    print (text)

    return text

image_path = (r"static/css/imgs/pan.jpg")  # Replace with your image path


# Check if file exists before processing
if os.path.exists(image_path):
    text = convert_image_to_text(image_path)
    print("Extracted Text:\n", text)
else:
    print(f"Error: File {image_path} does not exist.")
