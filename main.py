import telebot
from parser_selenium import login_form
bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')
@bot.message_handler(content_types=['text'])
def hello_message(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Добро пожаловать! "
              "Введите ваш логин или номер телефона, чтобы бот Вас узнал. После этого Вы сможете получать от бота уведомления и другую информацию.")
        login_msg = bot.send_message(message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(login_msg, login_take)
@bot.message_handler(content_types=['text'])
def login_take(message):

    login_take = message.text
    print(login_take)
    pwd_ask = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(pwd_ask, pwd_take, login_take)


@bot.message_handler(content_types=['text'])
def pwd_take(message, login_take):
    pwd_inp = message.text
    print(pwd_inp)
    print(login_form(login_take, pwd_inp))


bot.polling(none_stop=True, interval=0)