import re
import wolframalpha
import pytesseract
from PIL import Image

from local_package import get_resource

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def get_text():
    text = pytesseract.image_to_string(Image.open(get_resource("images", "img_recognition_2.jpg")))
    return text.replace("\n", " ").replace("  ", " ")


def re_search(text):
    print(text)
    pattern = r"((?=\d)\d+(,|\.)\d+((?=\s)|(,|\.)\d+))"
    math_result = re.findall(pattern, text)
    return [v[0] for v in math_result]


# print(re_search(get_text()))
client = wolframalpha.Client("TPLGT3-ETLWX6G6X3")
res = client.query("weather in Vinnytsya")
print(next(res.results).text)
