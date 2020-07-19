
from color import NamedColor
from random import choice
import ssl
import urllib.request


class XkcdColorList:
    def __init__(self):
        self.color_list = None

    def download_xkcd_color_list(self):
        """
        Downloads the xkcd color list (https://xkcd.com/color/rgb.txt).

        :return: None
        """
        xkcd = 'https://xkcd.com/color/rgb.txt'

        try:
            ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)

            self.color_list = urllib.request.urlopen(xkcd, context=ctx).read().decode().split('\n')[1:-1]
            self.color_list = map(lambda s: tuple(s[:-1].split('\t')), self.color_list)
            self.color_list = list(map(lambda t: (t[0].capitalize(), t[1].upper()), self.color_list))
        except IOError as err:
            print('{} — {}'.format(xkcd, err))

    def __getitem__(self, i):
        """
        Returns [i % len(color_list)] element as (name, html)

        :param i: int
        :return: color.NamedColor
        """
        assert isinstance(i, int)

        if not self.color_list:
            self.download_xkcd_color_list()

        return NamedColor(*self.color_list[i % len(self.color_list)]) if self.color_list else None

    def choice(self):
        """
        Returns a random element of the color list.

        :return: color.NamedColor
        """
        if not self.color_list:
            self.download_xkcd_color_list()

        return NamedColor(*choice(self.color_list)) if self.color_list else None

    def find_color(self, *, name=None, html=None):
        """
        Finds a color by its name or html in the color list.

        :param name: str
        :param html: str
        :return: color.NamedColor
        """
        if not self.color_list:
            self.download_xkcd_color_list()

        if self.color_list:
            for (name_, html_) in self.color_list:
                if name == name_ or html == html_:
                    return NamedColor(name=name_, html=html_)
        return NamedColor(name='Color is not found', html=html)


xkcd_color_list = XkcdColorList()
