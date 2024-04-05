import pytesseract

custom_config = r'--oem 3 --psm 6'
pytesseract.pytesseract.tesseract_cmd = r"D:\python_projects\Tesseract-OCR\tesseract.exe"

# Perform OCR on the image
text = pytesseract.image_to_string("modified_image.jpg", config=custom_config)

print(text)
