import time

import telebot
from telebot import types
import asyncio
from telebot.async_telebot import AsyncTeleBot
import mail_parse
from parser_selenium import login_form, request_parser
from qr_generator import qr_generator
from user_bd import user_add, user_search, delete_user

bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')
commands_list = ['/services', '/help', '/balance', '/plan', '/helpdesk']
all_us_inf = 0
message_q = ''
abonent_id = 0
import rest_class


def help_info(message, all_us_inf):
    all_us_inf = all_us_inf
    print(1)
    bot.send_message(message.from_user.id, f'Добро пожаловать {all_us_inf[3]}!')


def login_in(login, pwd):
    cookies = login_form(login, pwd)
    soup = request_parser(cookies)
    return cookies, soup


@bot.message_handler(content_types=['text'], commands=['start'])
def hello_message(message, another_try=1):
    # if message.text == "/start":
    global all_us_inf
    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд
    if all_us_inf[0]:  # Проверка на наличие юзера в бд

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        advice = types.KeyboardButton(text='Справка \U0001f4d6')
        keyboard.add(advice)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        bot.send_message(message.from_user.id,
                         'Этот бот работает в тестовом режиме, при сбоях писать на почту: osgaming47@gmail.com',
                         reply_markup=keyboard)

        help_info(message, all_us_inf)
    elif (all_us_inf[0] == False) and (another_try == 1):
        print(message.from_user.id)
        bot.send_message(message.from_user.id, "Добро пожаловать! "
                                               "Введите ваш логин или номер телефона, чтобы бот Вас узнал. После этого Вы сможете получать от бота уведомления и другую информацию.")
        login_msg = bot.send_message(message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(login_msg, login_take)
    elif (all_us_inf[0] == False) and (another_try == 0):
        login_msg = bot.send_message(message.chat.id, 'Введите логин:')
        bot.register_next_step_handler(login_msg, login_take)


def login_take(message):
    login_tak = message.text.upper()
    print(login_tak.upper())
    pwd_ask = bot.send_message(message.chat.id, 'Введите пароль:')
    bot.register_next_step_handler(pwd_ask, pwd_take, login_tak)


def pwd_take(message, login_take):
    pwd_inp = message.text
    print(pwd_inp.upper)
    final_login(message, pwd_inp, login_take)


def final_login(message, pwd_inp, login_take):
    cookies = login_form(login_take, pwd_inp)
    if cookies == False:
        bot.send_message(message.from_user.id, 'Введите логин и пароль еще раз')
        hello_message(message, 0)
    else:
        user_add(message.from_user.id, cookies, login_take, pwd_inp)
        resp = request_parser(cookies)
        bot.send_message(message.chat.id, f'Добро пожаловать! {login_take}')
        global abonent_id
        abonent_id = rest_class.abon_id(login_take)
        push_tg = rest_class.tg_id(abonent_id, message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        advice = types.KeyboardButton(text='Справка \U0001f4d6')
        keyboard.add(advice)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        bot.send_message(message.from_user.id,
                         'Этот бот работает в тестовом режиме, при сбоях писать на почту: osgaming47@gmail.com',
                         reply_markup=keyboard)

        soup = request_parser(cookies)

        global all_us_inf
        all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд


@bot.message_handler(content_types=['text'])
def al(message):

    global all_us_inf

    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд

    global message_q
    message_q = message
    print(message)

    if message.text == 'Справка \U0001f4d6':
        bot.send_message(message.chat.id,
                         f'Доступные команды:\n {commands_list[0]} - подключенные услуги \n {commands_list[1]} - справка \n {commands_list[2]} - текущий баланс \n {commands_list[3]} - текущий тариф \n {commands_list[4]}')
        asyncio.run(mail_check(message_q))
    elif message.text == 'Подключенные услуги \U0001f202\uFE0F':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_usluga(abonent_id)
        print(abonent_id)
        displ = '\n'.join(displ)
        bot.send_message(message.from_user.id,
                         f'Подключенные услуги:\n{displ} ')
        asyncio.run(mail_check(message_q))
        print(all_us_inf[3])
    elif message.text == 'QR':
        qr_generator(all_us_inf)
        photo = open('test1.png', 'rb')
        bot.send_photo(message.from_user.id, photo)
    elif message.text == 'Текущий баланс \U0001f4b0':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_balance(abonent_id)
        bot.send_message(message.from_user.id, f'Текущий баланс: {displ} руб.')
        asyncio.run(mail_check(message_q))


    elif message.text == 'Текущий тариф \U0001f310':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_tarif(abonent_id)
        bot.send_message(message.from_user.id, f'Текущий тариф: {displ}')
        asyncio.run(mail_check(message_q))

    elif message.text == 'Выйти из профиля \U0001f6aa':
        delete_user(message.chat.id)
        bot.send_message(message.from_user.id, 'Вы вышли из профиля')


async def mail_check(message):
    mail = mail_parse.mail_parse(all_us_inf[3])
    print(mail)
    count = 0
    for i in mail:
        count += 1
        print(i[0])
        bot.send_message(message.chat.id, 'Новое сообщение: ' + str(i[0].decode('utf-8')))


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

