# -*- encoding: utf-8 -*-

import time
import requests

from votacion import Votacion
import variables

bot = variables.bot

while True:
    try:
        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            chat_id = message.chat.id
            try:
                name = message.from_user.first_name
            except Exception as e:
                print(e)
                name = ''
            text = '¡Bienvenido %s!\n' \
                   'Agora US es un sistema de votación electronico que permite llevar el tradiccional' \
                   ' método de votación actual a un sistema online de forma segura.\n\n' \
                   'Este bot es una integración de dicho sistema y actualmente permite:\n' \
                   '/getvotes - 📰 Obtiene los votos de una encuesta test\n' \
                   '/votesi - 🔏 Vota SI en una encuesta test\n' \
                   '/voteno - 🔏 Vota NO en una encuesta test\n' \
                   '/votacion - 📝 Crea una votación' % name

            bot.send_photo(chat_id, 'http://imgur.com/VesqBnN.png')
            bot.reply_to(message, text)


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


        @bot.message_handler(commands=['votacion'])
        def crear_votacion(message):
            votacion_creator = Votacion()
            votacion_creator.crear_votacion(message)


        bot.polling(none_stop=True)
    except Exception as e:
        print('Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
