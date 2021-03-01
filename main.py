
import colored_image
import converter
import re
import telebot


import hidden
bot = telebot.TeleBot(hidden.bot_token)

markup = None
buttons_names = ['random xkcd', 'random', 'color of the day']


def make_markup():
    global markup
    markup = telebot.types.ReplyKeyboardMarkup()
    buttons = [telebot.types.KeyboardButton(name.capitalize()) for name in buttons_names]
    markup.row(*buttons[0:2])
    markup.row(buttons[2])


@bot.message_handler(commands=['start'])
def hello_message(message):
    """
    Prints hello message at start.

    :return: None
    """
    hello_msg = 'Hello!\nPrint the HTML or name of the color you want like «#FFB07C» or «Peach» or click a button.'
    bot.send_message(message.chat.id, text=hello_msg, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    """
    Prints help.

    :return: None
    """
    help_msg = """I'll send you a 500x500 image on your request with:
    1. «Random xkcd» or just «Random» color.
    2. A color by the name on [xkcd](xkcd.com/color/rgb).
    3. A color by its HTML color code.
    4. The «Color of the day».
    """
    bot.send_message(message.chat.id, text=help_msg, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(commands=['hide'])
def hide_keyboard(message):
    """
    Hides keyboard.

    :return: None
    """
    bot.send_message(message.chat.id, text='The keyboard was hidden', reply_markup=telebot.types.ReplyKeyboardRemove())


@bot.message_handler(commands=['show'])
def show_keyboard(message):
    """
    Shows keyboard.

    :return: None
    """
    bot.send_message(message.chat.id, text='The keyboard was appeared', reply_markup=markup)


@bot.message_handler(commands=['color'])
def color_command(message):
    """
    Sends image if command is not empty and prints a custom help if is.

    :return: None
    """
    if message.text.startswith('/color'):
        matched = re.findall('^/color (.*)', message.text)

        if matched:
            message.text = matched[0]
        else:
            msg = 'Print with this command a color by name on [xkcd](xkcd.com/color/rgb) or by html, ' \
                  'random [xkcd](xkcd.com/color/rgb) or just random color'
            bot.send_message(message.chat.id, text=msg, reply_markup=markup, parse_mode='Markdown',
                             reply_to_message_id=None if message.chat.type == 'private' else message.message_id)
            return
    send_image(message)


@bot.message_handler(content_types=['text'])
def send_image(message):
    """
    Sends image 500x500.

    Options: random, random xkcd, Image by color in HTML color format, color of the day.

    :return: None
    """
    try:
        if message.text.lower() == buttons_names[0]:  # random
            name, html, image = colored_image.colored_image(random=True)
        elif message.text.lower() == buttons_names[1]:  # random xkcd
            name, html, image = colored_image.colored_image(random=True, xkcd=False)
        elif message.text.lower() == buttons_names[2]:  # color of the day
            name, html, image = colored_image.colored_image(color_otd=True)
        elif converter.is_color_in_html(message.text):  # html
            name, html, image = colored_image.colored_image(html=message.text)
        else:  # requested color
            name, html, image = colored_image.colored_image(name=message.text)
    except IOError:  # if can't connect to xkcd.com, then send a random color picture
        bot.send_message(message.chat.id, text='Can\'t connect to xkcd.com', reply_markup=markup)
        name, html, image = colored_image.colored_image(random=True)

    bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html), reply_markup=markup,
                   reply_to_message_id=None if message.chat.type == 'private' else message.message_id)


def main():
    """
    Starts a bot and markup.
    """
    make_markup()
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
