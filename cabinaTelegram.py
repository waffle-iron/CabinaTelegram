# -*- encoding: utf-8 -*-

import telebot
import time
import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
token_id = config['Telegram']['token_id']

bot = telebot.TeleBot(token_id)

while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome!!')


        bot.polling(none_stop=True)
    except Exception as e:
        print('Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
