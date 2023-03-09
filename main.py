import threading

import time
from threading import Thread

import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import types

import mail_parse
import rest_class
from parser_selenium import login_form, request_parser, crm_selenium
from qr_generator import qr_generator
from user_bd import user_add, user_search, delete_user

sched = BackgroundScheduler()
bot = telebot.TeleBot('5911956484:AAFB0YU-9bldYHz4k4XfEaJ1yTqNPbWz00c')
commands_list = ['/services', '/help', '/balance', '/plan', '/helpdesk']
all_us_inf = 0
abonent_id = 0
tr = 0


def scheduler(login, message):
    schedule.every(1).minute.do(mail, login, message)
    global tr
    tr = 1
    print('Started scheduling')
    while True:
        schedule.run_pending()
        time.sleep(1)


import schedule


def mail(login, message):
    print(login, 'info for mail')
    sms = mail_parse.mail_parse(login)
    # print(sms)
    if len(sms) != 0:
        for i in sms:
            if 'Интернет доступ' not in i:
                bot.send_message(message.chat.id, 'Новое сообщение:' + '\n' + i)


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
    global message_q
    message_q = message

    if all_us_inf[0]:  # Проверка на наличие юзера в бд
        login = all_us_inf[3]
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)

        bot.send_message(message.from_user.id,
                         'Этот бот работает в тестовом режиме, при сбоях писать на почту: osgaming47@gmail.com',
                         reply_markup=keyboard)

        help_info(message, all_us_inf)
    elif (all_us_inf[0] == False) and (another_try == 1):
        print(message.from_user.id)
        bot.send_message(message.from_user.id, "Добро пожаловать! "
                                               "Заполните форму авторизации, чтобы бот Вас узнал. После этого Вы сможете получать от бота уведомления и другую информацию.")
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
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
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
        login = all_us_inf[3]
        Thread(target=scheduler, args=(login, message,)).start()

@bot.message_handler(content_types=['text'])
def al(message):
    global message_q
    message_q = message
    print(message)
    global all_us_inf

    all_us_inf = user_search(str(message.from_user.id))  # Сохранение данных юзера из бд
    if message.text == 'Подключенные услуги \U0001f202\uFE0F':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_usluga(abonent_id)
        print(abonent_id)
        displ = '\n'.join(displ)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        bot.send_message(message.from_user.id,
                         f'Подключенные услуги:\n{displ} ', reply_markup=keyboard)
        print(all_us_inf[3])
    elif message.text == 'Как оплатить? \U0001F4B0':
        video = open('WhatsApp Video 2023-03-06 at 14.51.32.mp4', 'rb')
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        bot.send_message(message.chat.id, f'Сбербанк онлайн:\n'
                         f'в платежах выбрать раздел Дом - Интернет, ТВ, домашний телефон.'
                         f' В поиске выбрать  "ООО "Старлинк Кантри" и ввести номер вашего  договора {all_us_inf[3]} '
                         f'После оплаты здесь чек не нужен, денежные средства сразу зачисляются на ваш абонентский счёт.')

        bot.send_video(message.chat.id, video)
        bot.send_message(message.chat.id, f'Личный кабинет:\n'
                                          f'Для оплаты через личный кабинет авторизуйтесь на сайте https://cabinet.levokumka.net '
                                          f'используя ваш логин: {all_us_inf[3]} и пароль: {all_us_inf[4]}\n'
                                          f'Перейдите во вкладку "Пополнение счета", укажите нужную сумму, почтовый ящик и нажмите оплатить, после чего вас перенаправит на защищенную страницу банка.', reply_markup=keyboard)

    elif message.text == 'QR':
        qr_generator(all_us_inf)
        photo = open('test1.png', 'rb')
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        bot.send_photo(message.from_user.id, photo, reply_markup=keyboard)
    elif message.text == 'Текущий баланс \U0001f4b0':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_balance(abonent_id)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        bot.send_message(message.from_user.id, f'Текущий баланс: {displ} руб.', reply_markup=keyboard)


    elif message.text == 'Текущий тариф \U0001f310':
        abonent_id = rest_class.abon_id(all_us_inf[3])
        displ = rest_class.abon_tarif(abonent_id)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        bot.send_message(message.from_user.id, f'Текущий тариф: {displ}', reply_markup=keyboard)

    elif message.text == 'Выйти из профиля \U0001f6aa':
        delete_user(message.chat.id)
        bot.send_message(message.from_user.id, 'Вы вышли из профиля')

    elif message.text == 'Запрос в тех. поддержку \U0001f477':
        subj_ask = bot.send_message(message.chat.id, 'Введите тему запроса:')
        bot.register_next_step_handler(subj_ask, subj)

def subj(message):
    subj_crm = message.text
    mes = bot.send_message(message.chat.id, 'Расскажите о своей проблеме:')
    bot.register_next_step_handler(mes, mes_ask, subj_crm)

def mes_ask(message, subj_crm):
    mes = message.text
    print(all_us_inf[3], all_us_inf[4])
    if crm_selenium(all_us_inf[3], all_us_inf[4], str(subj_crm), str(mes)):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
        serv = types.KeyboardButton(text='Подключенные услуги \U0001f202\uFE0F')
        keyboard.add(serv)
        bill = types.KeyboardButton(text='Текущий баланс \U0001f4b0')
        keyboard.add(bill)
        paln_btn = types.KeyboardButton(text='Текущий тариф \U0001f310')
        keyboard.add(paln_btn)
        crm = types.KeyboardButton(text='Запрос в тех. поддержку \U0001f477')
        keyboard.add(crm)
        pay = types.KeyboardButton(text='Как оплатить? \U0001F4B0')
        keyboard.add(pay)
        exit_btn = types.KeyboardButton(text='Выйти из профиля \U0001f6aa')
        keyboard.add(exit_btn)
        qr_btn = types.KeyboardButton(text='QR')
        keyboard.add(qr_btn)
        bot.send_message(message.chat.id, 'Запрос успешно отправлен', reply_markup=keyboard)


bot.polling()
