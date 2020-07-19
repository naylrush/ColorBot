
import converter


class NamedColor:
    def __init__(self, name=None, html=None, color=None):
        assert isinstance(name, str) if name else True
        assert isinstance(html, str) if html else True
        assert isinstance(color, tuple) if color else True
        self.name = name
        self.html = html
        self.color = color

        if html:
            self.html = html
            if not color:
                self.color = converter.html_to_color(self.html)
        elif color:
            for subcolor in list(color):
                assert 0 <= subcolor <= 255
            self.color = color
            self.html = converter.color_to_html(self.color)
