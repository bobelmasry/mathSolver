from PIL import Image
from pix2tex.cli import LatexOCR

img = Image.open('11.JPG')
model = LatexOCR()
print(model(img))