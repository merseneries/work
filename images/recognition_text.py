import re

import pytesseract
from PIL import Image

from my_funcs import get_resource

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_text():
    text = pytesseract.image_to_string(Image.open(get_resource("images", "img_recognition_2.jpg")))
    return text.replace("\n", " ").replace("  ", " ")


def re_search(text):
    print(text)
    pattern = r"((?=\d)\d+(,|\.)\d+((?=\s)|(,|\.)\d+))"
    math_result = re.findall(pattern, text)
    return [v[0] for v in math_result]


print(re_search(get_text()))
