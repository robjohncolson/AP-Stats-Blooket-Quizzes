import pytesseract
from PIL import Image

# Assuming you have an image file 'test.png'
text = pytesseract.image_to_string(Image.open('media/Ch10.png'))
print(text)