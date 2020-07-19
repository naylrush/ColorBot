
from PIL import Image, ImageDraw
from datetime import datetime
from random import randint
import converter
import inet
import io


def random_color():
    """
    Returns a random color.

    :return: str, (int, int, int)
    """
    color = (randint(0, 255), randint(0, 255), randint(0, 255))
    html = converter.color_to_html(color)
    return html, color


def random_xkcd_color():
    """
    Takes a random color from xkcd.com (https://xkcd.com/color/rgb.txt).

    :return: str, str, (int, int, int)
    """
    color = inet.xkcd_color_list.choice()

    if color:
        name, html = color
        return name, html, converter.html_to_color(html)

    html, color = random_color()
    return 'Can\'t connect to xkcd.com', html, color


def find_color(name=None, html=None):
    """
    Finds color by its name or html in the xkcd color list.

    :param name: str
    :param html: str
    :return: str, str, (int, int, int)
    """
    color = inet.xkcd_color_list.find_color(name=name, html=html)

    if color:
        name, html = color
        return name, html, converter.html_to_color(html)
    elif html:
        return 'Color is not found', html, converter.html_to_color(html)
    else:
        html, color = random_color()
        return 'Can\'t connect to xkcd.com', html, color


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

    :return: str, str, (int, int, int)
    """
    color = inet.xkcd_color_list[pseudorandom_number_of_today()]

    if color:
        name, html = color
        return name, html, converter.html_to_color(html)
    else:
        html, color = random_color()
        return 'Can\'t connect to xkcd.com', html, color


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
    color = None

    if color_otd:
        name, html, color = color_of_the_day()
    elif random:
        if xkcd:
            name, html, color = random_xkcd_color()
        else:
            name = 'Random color'
            html, color = random_color()
    else:
        if name:
            name, html, color = find_color(name=name.capitalize())
        if html:
            name, html, color = find_color(html=html.upper())

    ImageDraw.floodfill(image, xy=(0, 0), value=color)

    return name, html, image_to_bytes(image)
