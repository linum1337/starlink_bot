import telebot
from user_bd import user_add, user_search
from parser_selenium import login_form, request_parser, tarif_parse, balance_parse, req_payment_parse
bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')

@bot.message_handler(content_types=['text'])
def hello_message(message):
    if message.text == "/start":
        all_us_inf = user_search(str(message.from_user.id)) #Сохранение данных юзера из бд
        if all_us_inf[0]: #Проверка на наличие юзера в бд
            help_info(message, all_us_inf)
        else:
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
    after_login = login_in(login_take, pwd_inp)
    bot.send_message(message.chat.id, f'Добро пожаловать! {login_take}\n Текущий тариф: \n {tarif_parse(soup[0])}\n '
                                      f'Текущий баланс: {balance_parse(soup[1])} руб.')

@bot.message_handler(content_types=['text'])
def help_info(message, all_us_inf):
    print(1)
    bot.send_message(message.from_user.id, f'Добро пожаловать {all_us_inf[3]}! Доступные команды: /services')

@bot.message_handler(commands=['services'])
def services(message):
    print(111)
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = req_payment_parse(aft_inf[1][2])
    print(services_parsed)
    bot.send_message(message.from_user.id,
                        f'Подключенные услуги: \n {services_parsed[2][3: -4]} \n {services_parsed[3][3: -4]} \n {services_parsed[4][3: -4]} \n {services_parsed[5][3: -4]} ')


def login_in(login, pwd):
    cookies = login_form(login, pwd)
    soup = request_parser(cookies)
    return cookies, soup

'''@bot.message_handler(content_types=['text'])
def short_inf(message)'''
'''@bot.message_handler(content_types=['text'])
def usr_info()    '''

'''@bot.message_handler(content_types=['text'])
def balance_info(message, login_take, pwd_inp):
    if message == '/balance':
        print(balance_parse(login_form(login_take, pwd_inp)))'''

bot.polling(none_stop=True, interval=0)