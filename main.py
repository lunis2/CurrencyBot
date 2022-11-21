import telebot
from extensions import *

bot = telebot.TeleBot(env.TOKEN)

curr_lst = Converter.get_available_currencies()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(msg: telebot.types.Message):
    """Help handler for bot"""
    bot.reply_to(msg,
                 f"Hi {msg.from_user.username}, welcome to currency bot.\nUse desired currency name following by "
                 f"currency to convert plus amount. Example --> USD RUB 200\nUse /values too see the full list of "
                 f"currencies ")


@bot.message_handler(commands=['values'])
def values(msg: telebot.types.Message):
    """Values handler for bot"""
    resp = requests.get(env.VALUES_URL, headers=env.HEADERS)
    if resp.status_code == 200:
        txt = '\n'.join(f"{k}: {curr_lst[k]}" for k in curr_lst)
        bot.reply_to(msg, txt)
    else:
        resp.raise_for_status()


@bot.message_handler(content_types=['text'])
def convert(msg: telebot.types.Message):
    """Main handler for bot. Handles conversion requests."""
    user_request = msg.text.upper().split(" ")
    if len(user_request) != 3 or len(user_request[0]) != 3 or len(user_request[1]) != 3 or not user_request[2].isdigit():
        bot.reply_to(msg, "Please correct your request. For more information use /help")
    elif user_request[0] in curr_lst.keys() and user_request[1] in curr_lst.keys():
        text = Converter.get_price(user_request[0], user_request[1], user_request[2])
        bot.reply_to(msg, text)
    else:
        raise APIException("Wrong request")


bot.polling(none_stop=True)
