import telebot
from telebot import types
from user_bd import user_add, user_search, delete_user
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from parser_selenium import login_form, request_parser, tarif_parse, balance_parse, req_payment_parse, req_payment_ryl, \
    helpdesk_sender

bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')
commands_list = ['/services', '/help', '/balance', '/plan', '/helpdesk']
all_us_inf = 0


def help_info(message, all_us_inf):
    all_us_inf = all_us_inf
    print(1)
    bot.send_message(message.from_user.id, f'Добро пожаловать {all_us_inf[3]}! Для справки воспользуйтесь /help')


def login_in(login, pwd):
    cookies = login_form(login, pwd)
    soup = request_parser(cookies)
    return cookies, soup


@bot.message_handler(content_types=['text'], commands=['start'])
def hello_message(message):
    # if message.text == "/start":
    global all_us_inf
    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд
    if all_us_inf[0]:  # Проверка на наличие юзера в бд

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        advice = types.KeyboardButton(text='Справка')
        keyboard.add(advice)
        serv = types.KeyboardButton(text='Подключенные услуги')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф')
        keyboard.add(paln_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля')
        keyboard.add(exit_btn)
        bot.send_message(message.from_user.id,
                         'Этот бот работает в тестовом режиме, при сбоях писать на почту: osgaming47@gmail.com',
                         reply_markup=keyboard)

        help_info(message, all_us_inf)
    else:
        print(message.from_user.id)
        bot.send_message(message.from_user.id, "Добро пожаловать! "
                                               "Введите ваш логин или номер телефона, чтобы бот Вас узнал. После этого Вы сможете получать от бота уведомления и другую информацию.")
        login_msg = bot.send_message(message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(login_msg, login_take)


def login_take(message):
    login_take = message.text.upper()
    print(login_take.upper())
    pwd_ask = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(pwd_ask, pwd_take, login_take)


def pwd_take(message, login_take):
    pwd_inp = message.text
    print(pwd_inp.upper)
    cookies = login_form(login_take, pwd_inp)
    if cookies == 0:
        bot.send_message(message.from_user.id, 'Данные не верны, повторите попытку')
        hello_message()

    resp = request_parser(cookies)
    bot.send_message(message.chat.id, f'Добро пожаловать! {login_take}')
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    advice = types.KeyboardButton(text='Справка')
    keyboard.add(advice)
    serv = types.KeyboardButton(text='Подключенные услуги')
    keyboard.add(serv)
    bill = types.KeyboardButton(text='Текущий баланс')
    keyboard.add(bill)
    paln_btn = types.KeyboardButton(text='Текущий тариф')
    keyboard.add(paln_btn)
    exit_btn = types.KeyboardButton(text='Выйти из профиля')
    keyboard.add(exit_btn)
    bot.send_message(message.from_user.id,
                     'Этот бот работает в тестовом режиме, при сбоях писать на почту: osgaming47@gmail.com',
                     reply_markup=keyboard)

    soup = request_parser(cookies)

    user_add(message.from_user.id, cookies, login_take, pwd_inp)
    global all_us_inf
    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд


@bot.message_handler(content_types=['text'])
def al(message):
    global all_us_inf
    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд
    if message.text == 'Справка':
        bot.send_message(message.chat.id,
                         f'Доступные команды:\n {commands_list[0]} - подключенные услуги \n {commands_list[1]} - справка \n {commands_list[2]} - текущий баланс \n {commands_list[3]} - текущий тариф \n {commands_list[4]}')
    elif message.text == 'Подключенные услуги':
        bot.send_message(message.from_user.id, 'Выполняем запрос')
        print(all_us_inf)
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = req_payment_parse(aft_inf[1][2])[2::]
        print(services_parsed)
        displ = ''
        for i in services_parsed:
            displ = displ + '\n' + str(str(str(i).split('<i>')[1]).split('</i>')[0])
        bot.send_message(message.from_user.id,
                         f'Подключенные услуги: {displ} ')

    elif message.text == 'Текущий баланс':
        bot.send_message(message.from_user.id, 'Выполняем запрос')
        all_us_inf = user_search(str(message.from_user.id))
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = balance_parse(aft_inf[1][1])
        print(services_parsed)
        bot.send_message(message.from_user.id, f'Текущий баланс: {services_parsed} руб.')

    elif message.text == 'Текущий тариф':
        bot.send_message(message.from_user.id, 'Выполняем запрос')
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = tarif_parse(aft_inf[1][0])
        print(services_parsed)
        bot.send_message(message.from_user.id, f'Текущий тариф: {services_parsed}')

    elif message.text == 'Выйти из профиля':
        delete_user(message.chat.id)
        bot.send_message(message.from_user.id, 'Вы вышли из профиля')


'''@bot.message_handler(commands=['helpdesk'])
def helpdesk(message):
    all_us_inf = user_search(str(message.from_user.id))
    cookies = login_form(all_us_inf[3], all_us_inf[4])
    a = helpdesk_sender(cookies)
    if a:
        bot.send_message(message.from_user.id, "Запрос отправлен")
'''
'''
@bot.message_handler(content_types=['text'])
def help(message):
    if message.text == 'Справка':
        bot.send_message(message.chat.id,
                         f'Доступные команды:\n {commands_list[0]} - подключенные услуги \n {commands_list[1]} - справка \n {commands_list[2]} - текущий баланс \n {commands_list[3]} - текущий тариф \n {commands_list[4]}')

@bot.message_handler(content_types=['text'])
def services(message):
    # bot.send_message(message.chat.id, 'я тут')
    if message.text == 'Подключенные услуги':
        all_us_inf = user_search(str(message.from_user.id))
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = req_payment_parse(aft_inf[1][2])
        print(services_parsed)
        bot.send_message(message.from_user.id,
                         f'Подключенные услуги: \n {str(services_parsed[2])[3: -4]} \n {str(services_parsed[3])[3: -4]} \n {str(services_parsed[4])[3: -4]} \n {str(services_parsed[5])[3: -4]} ')

#@bot.message_handler(content_types=['text'])
def balance(message):
    if message.text == 'Текущий баланс':
        all_us_inf = user_search(str(message.from_user.id))
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = balance_parse(aft_inf[1][1])
        print(services_parsed)
        bot.send_message(message.from_user.id, f'Текущий баланс: {services_parsed} руб.')

#@bot.message_handler(content_types=['text'])
def plan(message):
    if message.text == 'Текущий тариф':
        all_us_inf = user_search(str(message.from_user.id))
        aft_inf = login_in(all_us_inf[3], all_us_inf[4])
        services_parsed = tarif_parse(aft_inf[1][0])
        print(services_parsed)
        bot.send_message(message.from_user.id, f'Текущий тариф: {services_parsed}')






@bot.message_handler(commands=['pay'])
def req_pay(message):
    all_us_inf = user_search(str(message.from_user.id))
    aft_inf = login_in(all_us_inf[3], all_us_inf[4])
    services_parsed = req_payment_ryl(aft_inf[1][0])
    print(services_parsed)
    bot.send_message(message.from_user.id, f'Текущий тариф: {services_parsed}')


'''

bot.polling()
