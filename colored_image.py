
from PIL import Image, ImageDraw
from random import randint
import io
import re


def random_color():
    """
    Returns random color.

    :return: (int, int, int)
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)


def color_to_html(color):
    """
    Convert color to HTML color code.

    :param color: (int, int, int)
    :return: str
    """
    if len(color) != 3:
        raise Exception('Three color properties required')

    return '#' + ('{:0<2}'*3).format(*map(lambda s: format(s, 'x'), color)).upper()


def is_color_in_html(html):
    """
    Checks color is in HTML color format.

    :param html: str
    :return: bool
    """
    coincidences = re.findall('#[0-9a-fA-F]*', html)
    return coincidences and coincidences[0] == html and len(html) == 7


def html_to_color(html):
    """
    Convert HTML color code to color.

    :param html: str
    :return: (int, int, int)
    """
    if not is_color_in_html(html):
        raise Exception('The color is not in HTML color format!')

    color = []
    for i in range(3):
        color.append(html[1 + i*2:i*2 + 3])

    return tuple(map(lambda s: int(s, 16), color))


def colored_image(color=None, html=None):
    """
    Generates 500x500 image filled in with a given or random color.

    :return: bytes, str
    """
    width, height = 500, 500
    image = Image.new('RGB', (width, height))

    if not color:
        if html:
            color = html_to_color(html)
        else:
            color = random_color()

    ImageDraw.floodfill(image, xy=(0, 0), value=color)

    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format='PNG')
    bytes_image = bytes_buffer.getvalue()

    return bytes_image, color_to_html(color)
