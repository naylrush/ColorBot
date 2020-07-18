
import colored_image
import converter
import telebot


# Make a bot
import hidden
bot = telebot.TeleBot(hidden.bot_token)

# Make a markup
markup = telebot.types.ReplyKeyboardMarkup()
random_button = telebot.types.KeyboardButton('Random xkcd')
markup.row(random_button)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """
    Sends image 500x500.

    Options: Random, Image by color in HTML color format.

    :return: None
    """
    if message.text == 'Random':
        name, html, image = colored_image.colored_image()
        bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html))
    elif converter.is_color_in_html(message.text):
        name, html, image = colored_image.colored_image(html=message.text)
        bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html))
    else:
        bot.send_message(message.chat.id, text='Choose a button:', reply_markup=markup)


if __name__ == '__main__':
    # Start the bot
    bot.polling(none_stop=True, interval=0)
