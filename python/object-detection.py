from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os
from rapid_latex_ocr import LatexOCR
import pytesseract

# Load a pretrained YOLOv8n model
model = YOLO('best3.pt')

parent_dir = r"D:\python_projects\other shit\mathSolverRepo\python"

# Create the parent directory if it doesn't exist
if not os.path.exists(parent_dir):
    os.makedirs(parent_dir)

# Path to the image
image_path = 'image.jpg'
image_full_path = os.path.join(parent_dir, image_path)

# Create a directory with the same name as the image file
image_dir = os.path.splitext(image_full_path)[0]  # Remove the extension from the image file name
os.makedirs(image_dir, exist_ok=True)  # Create the directory if it doesn't exist, overwrite if it already exists

# Run inference on an image
results = model(image_path)

# Filter results based on custom confidence thresholds
filtered_boxes = []
for box in results[0].boxes:
    class_id = int(box.cls)
    if box.conf >= 0.5:
        filtered_boxes.append(box)

image = Image.open(image_path)

# Create a blank mask
mask = Image.new('L', image.size, 0)

draw = ImageDraw.Draw(image)

# Iterate over the list of detected boxes and draw rectangles on the mask
iterator = 1
iterator2 = 1

# Font settings
font_size = 20
font = ImageFont.truetype("arial.ttf", font_size)

# Iterate over the list of detected boxes, draw rectangles on the mask, and add placeholder text
for box in filtered_boxes:
    x_min, y_min, x_max, y_max = [int(coord) for coord in box.xyxy.tolist()[0]]
    # Crop the image to the bounding box region
    cropped_image = image.crop((x_min, y_min, x_max, y_max))
    
    # Save the cropped image with an iterator as the filename
    cropped_image.save(f"{image_dir}/formula{iterator2}.jpg")
    iterator2 += 1

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            # Change the color of the pixel to white (255, 255, 255)
            image.putpixel((x, y), (255, 255, 255))

    
    # Calculate text size and position to fill the bounding box
    text = f"Ak={iterator}"
    text_x = (x_max + x_min) // 2 - 15  # Center text horizontally
    text_y = (y_max + y_min) // 2 - 15  # Center text vertically
    draw.text((text_x, text_y), text, fill=0, font=font)  # Draw placeholder text in the center of the bounding box
    iterator += 1

# Apply the mask to the image
image.paste((255, 255, 255), mask=mask)

# Save or display the modified image
image.show()
image.save(f'{image_dir}/modified_image.jpg')

latexModel = LatexOCR()
latex = []
for i in range(len(os.listdir(image_dir)) - 1):
    dir = os.listdir(image_dir)
    imagePath = f"{image_dir}/{dir[i]}"
    with open(imagePath, "rb") as f:
        data = f.read()

    res, elapse = latexModel(data)

    latexFromImage = res
    latex.append(res)

custom_config = r'--oem 3 --psm 6'
pytesseract.pytesseract.tesseract_cmd = r"D:\python_projects\Tesseract-OCR\tesseract.exe"

text = pytesseract.image_to_string(f"{image_dir}/modified_image.jpg", config=custom_config)

for i in range(1, len(latex) + 1):
    pattern1 = "Ak=" + str(i)
    pattern2 = "Ak-" + str(i)
    pattern3 = "AK=" + str(i)
    pattern4 = "AK-" + str(i)
    pattern5 = f"AK{str(i)}"
    pattern6 = f"Ak{str(i)}"
    if pattern1 in text:
        text = text.replace(pattern1, latex[i - 1])
    if pattern2 in text:
        text = text.replace(pattern2, latex[i - 1])
    if pattern3 in text:
        text = text.replace(pattern3, latex[i - 1])
    if pattern4 in text:
        text = text.replace(pattern4, latex[i - 1])
    if pattern5 in text:
        text = text.replace(pattern5, latex[i - 1])
    if pattern6 in text:
        text = text.replace(pattern6, latex[i - 1])

print(text)