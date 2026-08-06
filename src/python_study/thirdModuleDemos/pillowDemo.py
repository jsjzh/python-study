from PIL import Image, ImageFilter

from python_study.utils import getAssetsPath


def thumbnailImg():
    img = Image.open(getAssetsPath(["car.png"]))
    w, h = img.size
    img.thumbnail((w / 2, h / 2))
    return img


def blurImg():
    img = Image.open(getAssetsPath(["car.png"]))
    return img.filter(ImageFilter.BLUR)


def main() -> None:
    thumbnailImg().save(getAssetsPath(["car-thumb.png"]))
    blurImg().save(getAssetsPath(["car-blur.png"]))
    # img.show("car")
    pass
