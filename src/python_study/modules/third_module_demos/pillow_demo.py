import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from python_study.utils import get_assets_path


def thumbnail_img():
    img = Image.open(get_assets_path(["car.png"]))
    w, h = img.size
    img.thumbnail((w / 2, h / 2))
    return img


def blur_img():
    img = Image.open(get_assets_path(["car.png"]))
    return img.filter(ImageFilter.BLUR)


# 随机字母:
def rnd_char():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rnd_color():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rnd_color_2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def draw_img():
    w = 240
    h = 60
    img = Image.new("RGB", (w, h), (255, 255, 255))
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 36)
    draw = ImageDraw.Draw(img)

    for x in range(w):
        for y in range(h):
            draw.point((x, y), fill=rnd_color())

    for t in range(4):
        draw.text(xy=(60 * t + 12, 5), text=rnd_char(), font=font, fill=rnd_color_2())

    return img.filter(ImageFilter.BLUR)


def main() -> None:
    # thumbnail_img().save(get_assets_path(["car-thumb.png"]))
    # blur_img().save(get_assets_path(["car-blur.png"]))
    draw_img().save(get_assets_path(["draw.png"]))
    # img.show("car")
    pass
