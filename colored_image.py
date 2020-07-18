
from PIL import Image, ImageDraw
from random import randint
import io


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


def colored_image(color=None):
    """
    Generates 500x500 image filled in with a given or random color.

    :return: bytes, str
    """
    width, height = 500, 500
    image = Image.new('RGB', (width, height))

    color = color if color else random_color()
    ImageDraw.floodfill(image, xy=(0, 0), value=color)

    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format='PNG')
    bytes_image = bytes_buffer.getvalue()

    return bytes_image, color_to_html(color)
