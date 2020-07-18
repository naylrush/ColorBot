
from PIL import Image, ImageDraw
from random import randint, choice
import converter
import io
import ssl
import urllib.request


xkcd_color_list = None


def download_xkcd_color_list():
    """
    Downloads the xkcd color list (https://xkcd.com/color/rgb.txt).

    :return: None
    """
    xkcd = 'https://xkcd.com/color/rgb.txt'

    try:
        global xkcd_color_list
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)
        xkcd_color_list = urllib.request.urlopen(xkcd, context=ctx).read().decode().split('\n')[1:-1]
        xkcd_color_list = map(lambda s: tuple(s[:-1].split('\t')), xkcd_color_list)
        xkcd_color_list = list(map(lambda t: (t[0].capitalize(), t[1].upper()), xkcd_color_list))
    except IOError as err:
        print('{} — {}'.format(xkcd, err))


def random_color():
    """
    Takes a random color from xkcd.com (https://xkcd.com/color/rgb.txt).

    :return: str, str, (int, int, int)
    """

    if not xkcd_color_list:
        download_xkcd_color_list()

    if xkcd_color_list:
        name, html = choice(xkcd_color_list)
        return name, html, converter.html_to_color(html)
    else:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))
        return 'Can\'t connect to xkcd.com', converter.color_to_html(color), color


def colored_image(color=None, html=None):
    """
    Generates 500x500 image filled in with a given or random color from xkcd.

    :return: str, str, bytes
    """
    width, height = 500, 500
    image = Image.new('RGB', (width, height))

    name = 'Unknown color'
    if not color:
        if html:
            color = converter.html_to_color(html)
        else:
            name, html, color = random_color()

    ImageDraw.floodfill(image, xy=(0, 0), value=color)

    bytes_buffer = io.BytesIO()
    image.save(bytes_buffer, format='PNG')
    bytes_image = bytes_buffer.getvalue()

    return name, html.upper(), bytes_image
