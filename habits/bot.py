import telebot

bot = telebot.TeleBot('6947279879:AAESKXowF4zovjLuuTeGh6ipDehEJAouu5I')


@bot.message_handler(content_types=['text'])


def handle_text(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет, чем я могу тебе помочь?")
    elif message.text.lower() == "/help":
        bot.send_message(message.chat.id, "Напиши привет")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю. Напиши /help.")


# Уберите декоратор @bot.message_handler, который находится внутри другого декоратора
@bot.message_handler(content_types=['document', 'audio'])


def handle_other_types(message):
    pass
