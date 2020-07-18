
import colored_image
import converter
import telebot


# Make a bot
import hidden
bot = telebot.TeleBot(hidden.bot_token)

# Make a markup
markup = telebot.types.ReplyKeyboardMarkup()
buttons_names = ['Random xkcd', 'Random']
buttons = [telebot.types.KeyboardButton(name) for name in buttons_names]
markup.row(*buttons[0:2])


@bot.message_handler(content_types=['text'])
def send_image(message):
    """
    Sends image 500x500.

    Options: Random, Image by color in HTML color format.

    :return: None
    """
    if message.text == buttons_names[0]:
        name, html, image = colored_image.colored_image(random=True)
    elif message.text == buttons_names[1]:
        name, html, image = colored_image.colored_image(random=True, xkcd=False)
    elif converter.is_color_in_html(message.text):
        name, html, image = colored_image.colored_image(html=message.text)
    else:
        name, html, image = colored_image.colored_image(name=message.text)
    bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html), reply_markup=markup)


if __name__ == '__main__':
    # Start the bot
    bot.polling(none_stop=True, interval=0)
