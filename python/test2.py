from rapid_latex_ocr import LatexOCR

model = LatexOCR()

img_path = r"11.JPG"
with open(img_path, "rb") as f:
    data = f.read()

res, elapse = model(data)

print(res)
print(elapse)