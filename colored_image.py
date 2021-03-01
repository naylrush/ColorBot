
from PIL import Image, ImageDraw
from datetime import datetime
from random import randint
from color import NamedColor
import hashlib
import io
import xkcd


def random_color(*, name='Random color'):
    """
    Returns a random color.

    :return: color.NamedColor
    """
    return NamedColor(name=name, color=(randint(0, 255), randint(0, 255), randint(0, 255)))


def random_xkcd_color():
    """
    Takes a random color from xkcd.com (https://xkcd.com/color/rgb.txt).

    :return: color.NamedColor
    """
    return xkcd.xkcd_color_list.choice()


def find_color(name=None, html=None):
    """
    Finds color by its name or html in the xkcd color list.

    :param name: str
    :param html: str
    :return: color.NamedColor
    """
    return xkcd.xkcd_color_list.find_color(name=name, html=html)


def image_to_bytes(image):
    """
    Converts PIL image to bytes

    :param image: PIL.Image
    :return: bytes
    """
    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format='PNG')
    return bytes_buffer.getvalue()


def pseudorandom_number_of_today():
    """
    Returns the pseudorandom number of the today.

    :return: int
    """
    multiplier = int('5DEECE66', 16)
    addend = 11
    mask = (1 << 48) - 1

    today = datetime.today()
    date = sum(datetime(today.year, today.month, today.day).isocalendar())

    return ((date * multiplier + addend) & mask) << 16


def color_of_the_day():
    """
    Returns color of the day.

    :return: color.NamedColor
    """
    return xkcd.xkcd_color_list[pseudorandom_number_of_today()]


def colored_image(name=None, html=None, random=False, xkcd=True, color_otd=False):
    """
    Generates 500x500 image filled in with a given or random color.

    :param name: str
    :param html: str
    :param random: bool
    :param xkcd: bool
    :param color_otd: bool
    :return: str, str, bytes
    """
    width, height = 500, 500
    image = Image.new('RGB', (width, height))

    if color_otd:
        color = color_of_the_day()
    elif random:
        color = random_xkcd_color() if xkcd else random_color()
    else:
        color = find_color(name=name.capitalize() if name else None, html=html.upper() if html else None)
        if not color:
            if not html:
                sha = hashlib.sha256()
                sha.update(name.encode())
                html = '#' + sha.hexdigest()[:6]
            color = NamedColor(name=name, html=html.upper())

    ImageDraw.floodfill(image, xy=(0, 0), value=color.color)

    return color.name, color.html, image_to_bytes(image)
