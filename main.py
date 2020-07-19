
import colored_image
import converter
import telebot


# Make a bot
import hidden
bot = telebot.TeleBot(hidden.bot_token)

# Markup
markup = telebot.types.ReplyKeyboardMarkup()
buttons_names = ['random xkcd', 'random', 'color of the day']
buttons = [telebot.types.KeyboardButton(name.capitalize()) for name in buttons_names]
markup.row(*buttons[0:2])
markup.row(buttons[2])


@bot.message_handler(commands=['start'])
def hello_message(message):
    hello_msg = 'Hello!\nPrint the HTML or name of the color you want like «#FFB07C» or «Peach» or click a button.'
    bot.send_message(message.chat.id, text=hello_msg, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_msg = """I'll send you a 500x500 image on your request with:
    1. «Random xkcd» or just «Random» color.
    2. A color by the name on [xkcd](xkcd.com/color/rgb).
    3. A color by its HTML color code.
    4. The «Color of the day».
    """
    bot.send_message(message.chat.id, text=help_msg, reply_markup=markup, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def send_image(message):
    """
    Sends image 500x500.

    Options: Random, Image by color in HTML color format.

    :return: None
    """
    if message.text.lower() == buttons_names[0]:
        name, html, image = colored_image.colored_image(random=True)
    elif message.text.lower() == buttons_names[1]:
        name, html, image = colored_image.colored_image(random=True, xkcd=False)
    elif message.text.lower() == buttons_names[2]:
        name, html, image = colored_image.colored_image(color_otd=True)
    elif converter.is_color_in_html(message.text):
        name, html, image = colored_image.colored_image(html=message.text)
    else:
        name, html, image = colored_image.colored_image(name=message.text)
    bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html), reply_markup=markup)


if __name__ == '__main__':
    # Start the bot
    bot.polling(none_stop=True, interval=0)
