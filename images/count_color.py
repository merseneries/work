import json

from PIL import Image

from local_package import get_path

NAME_IMAGE = "black-picture.png"


def image_stat(name):
    full_path = get_path(name)
    img = Image.open(full_path)
    img = img.convert("L")
    img.save(get_path("output.png"))

    img_bits = {"white": 0, "black": 0, "other": 0}

    for h in range(img.height):
        for w in range(img.width):
            pixel = img.getpixel((w, h))
            if pixel == 0:
                img_bits["black"] = img_bits.get("black") + 1
            elif pixel == 255:
                img_bits["white"] = img_bits.get("white") + 1
            else:
                img_bits["other"] = img_bits.get("other") + 1

    print(json.dumps(img_bits, indent=4))


image_stat(NAME_IMAGE)
