
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
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS)

        global xkcd_color_list
        xkcd_color_list = urllib.request.urlopen(xkcd, context=ctx).read().decode().split('\n')[1:-1]
        xkcd_color_list = map(lambda s: tuple(s[:-1].split('\t')), xkcd_color_list)
        xkcd_color_list = list(map(lambda t: (t[0].capitalize(), t[1].upper()), xkcd_color_list))
    except IOError as err:
        print('{} — {}'.format(xkcd, err))
