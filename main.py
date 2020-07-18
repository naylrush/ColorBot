
from PIL import Image, ImageDraw
from random import randint
import io
import telebot


# Make a bot
import hidden
bot = telebot.TeleBot(hidden.bot_token)

# Make a markup
markup = telebot.types.ReplyKeyboardMarkup()
random_button = telebot.types.KeyboardButton('Random')
markup.row(random_button)


def random_color():
    """
    Returns random color.

    :return: (int, int, int, int)
    """
    return randint(0, 255), randint(0, 255), randint(0, 255)


def color_to_html_code(color):
    """
    Convert color to HTML code.

    :param color: [int]
    :return: str
    """
    if len(color) != 3:
        raise Exception('Three color properties required')

    return '#' + ''.join(map(lambda x: x[2:], map(hex, color))).upper()


def generate_colored_image(color=None):
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

    return bytes_image, color_to_html_code(color)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """
    Sends image 500x500.

    Options: Random.

    :return: None
    """
    if message.text == 'Random':
        image, html_code = generate_colored_image()
        bot.send_photo(message.chat.id, caption=html_code, photo=image)
    else:
        bot.send_message(message.chat.id, text='Choose a button:', reply_markup=markup)


if __name__ == '__main__':
    # Start the bot
    bot.polling(none_stop=True, interval=0)
