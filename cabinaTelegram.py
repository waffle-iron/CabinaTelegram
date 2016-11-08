# -*- encoding: utf-8 -*-

import telebot
import time
import requests

API_TOKEN = '219345528:AAEI9PX3pYLoOAtIrgGGyJQF9Fu9PjvHmDc'
bot = telebot.TeleBot(API_TOKEN)

admin_id = 14069151

while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome!!')


        # EJEMPLO DE GET_VOTES
        @bot.message_handler(commands=['getvotes'])
        def get_votes(message):
            url = 'http://188.213.161.241/API/get_votes.php?votation_id=8'
            result = requests.get(url)
            bot.reply_to(message, result)


        # EJEMPLO DE SEND_VOTE
        @bot.message_handler(commands=['votesi'])
        def send_vote(message):
            url = 'http://188.213.161.241/API/vote.php'
            payload = {'votationName': 'testBot', 'vote': 'SI', 'zipcode': '28033'}
            result = requests.post(url, payload)
            bot.reply_to(message, result)


        @bot.message_handler(commands=['voteno'])
        def send_vote(message):
            url = 'http://188.213.161.241/API/vote.php'
            payload = {'votationName': 'testBot', 'vote': 'NO', 'zipcode': '28033'}
            result = requests.post(url, payload)
            bot.reply_to(message, result)


        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(admin_id, 'Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
