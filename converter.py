
import re


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
