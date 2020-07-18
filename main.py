
import telebot
import colored_image


# Make a bot
import hidden
bot = telebot.TeleBot(hidden.bot_token)

# Make a markup
markup = telebot.types.ReplyKeyboardMarkup()
random_button = telebot.types.KeyboardButton('Random')
markup.row(random_button)


@bot.message_handler(content_types=['text'])
def send_message(message):
    """
    Sends image 500x500.

    Options: Random, Image by color in HTML color format.

    :return: None
    """
    if message.text == 'Random':
        image, html, name = colored_image.colored_image()
        bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html))
    elif colored_image.is_color_in_html(message.text):
        image, html, name = colored_image.colored_image(html=message.text)
        bot.send_photo(message.chat.id, photo=image, caption='{} — {}'.format(name, html))
    else:
        bot.send_message(message.chat.id, text='Choose a button:', reply_markup=markup)


if __name__ == '__main__':
    # Start the bot
    bot.polling(none_stop=True, interval=0)
