# -*- encoding: utf-8 -*-

import telebot
import time

API_TOKEN = '242035355:AAGgFud76CXCIuwRUn1WJl6XjjWnQVRsKYE'
bot = telebot.TeleBot(API_TOKEN)

admin_id = 14069151

while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome!!')


        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(admin_id, 'Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
