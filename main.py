import telebot, types
from user_bd import user_add, user_search
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from parser_selenium import login_form, request_parser, tarif_parse, balance_parse, req_payment_parse,req_payment_ryl
bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')
commands_list = ['/services', '/help', '/balance', '/plan']
@bot.message_handler(content_types=['text'], commands=['start'])
def hello_message(message):
    #if message.text == "/start":
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Btn1', callback_data='Btn'))
    all_us_inf = user_search(str(message.from_user.id)) #Сохранение данных юзера из бд
    if all_us_inf[0]: #Проверка на наличие юзера в бд
        help_info(message, all_us_inf)
    else:
        bot.send_message(message.from_user.id, "Добро пожаловать! "
                "Введите ваш логин или номер телефона, чтобы бот Вас узнал. После этого Вы сможете получать от бота уведомления и другую информацию.")
        login_msg = bot.send_message(message.chat.id, 'Введите логин:')
        login_take = message.text

        bot.register_next_step_handler(login_msg, login_take)
        pwd_ask = bot.send_message(message.chat.id, 'Введите пароль:')
        pwd_inp = message.text
        after_login = login_in(login_take, pwd_inp)
        bot.send_message(message.chat.id, f'Добро пожаловать! {login_take}\n Текущий тариф: ')
        help_info(message, all_us_inf)

@bot.message_handler(commands=['services'])
def services(message):
    #bot.send_message(message.chat.id, 'я тут')
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = req_payment_parse(aft_inf[1][2])
    print(services_parsed)
    bot.send_message(message.from_user.id,
                     f'Подключенные услуги: \n {str(services_parsed[2])[3: -4]} \n {str(services_parsed[3])[3: -4]} \n {str(services_parsed[4])[3: -4]} \n {str(services_parsed[5])[3: -4]} ')


@bot.message_handler(commands=['balance'])
def balance(message):
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = balance_parse(aft_inf[1][1])
    print(services_parsed)
    bot.send_message(message.from_user.id, f'Текущий баланс: {services_parsed} руб.')

@bot.message_handler(commands=['pay'])
def req_pay(message):
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = req_payment_ryl(aft_inf[1][0])
    print(services_parsed)
    bot.send_message(message.from_user.id, f'Текущий тариф: {services_parsed}')
@bot.message_handler(commands=['plan'])
def plan(message):
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = tarif_parse(aft_inf[1][0])
    print(services_parsed)
    bot.send_message(message.from_user.id, f'Текущий тариф: {services_parsed}')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Доступные команды:\n {commands_list[0]} - подключенные услуги \n {commands_list[1]} - справка \n {commands_list[2]} - текущий баланс \n {commands_list[3]} - текущий тариф')
@bot.message_handler(content_types=['text'])
def help_info(message, all_us_inf):
    all_us_inf = all_us_inf
    print(1)
    bot.send_message(message.from_user.id, f'Добро пожаловать {all_us_inf[3]}! Для справки воспользуйтесь /help')



def login_in(login, pwd):
    cookies = login_form(login, pwd)
    soup = request_parser(cookies)
    return cookies, soup


bot.polling(none_stop=True, interval=0)