import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from python_study.utils import getAssetsPath


def thumbnailImg():
    img = Image.open(getAssetsPath(["car.png"]))
    w, h = img.size
    img.thumbnail((w / 2, h / 2))
    return img


def blurImg():
    img = Image.open(getAssetsPath(["car.png"]))
    return img.filter(ImageFilter.BLUR)


# 随机字母:
def rndChar():
    return chr(random.randint(65, 90))


# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


def drawImg():
    w = 240
    h = 60
    img = Image.new("RGB", (w, h), (255, 255, 255))
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 36)
    draw = ImageDraw.Draw(img)

    for x in range(w):
        for y in range(h):
            draw.point((x, y), fill=rndColor())

    for t in range(4):
        draw.text(xy=(60 * t + 12, 5), text=rndChar(), font=font, fill=rndColor2())

    return img.filter(ImageFilter.BLUR)


def main() -> None:
    # thumbnailImg().save(getAssetsPath(["car-thumb.png"]))
    # blurImg().save(getAssetsPath(["car-blur.png"]))
    drawImg().save(getAssetsPath(["draw.png"]))
    # img.show("car")
    pass
