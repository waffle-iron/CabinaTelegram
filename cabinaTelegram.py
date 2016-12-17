# -*- encoding: utf-8 -*-

import time

import requests
from telebot import types

import variables
from src.utils import Utils
from src.votacion import Votacion

bot = variables.bot

utils = Utils()

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
                   '/votacion - 📝 Crea una votación\n' \
                   '/misvotaciones - Muestra mis votaciones creadas\n' \
                   '/compartir - Muestra panel para compartir votaciones' % name

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
            user_id = message.from_user.id
            votacion = Votacion()
            votacion.crear_votacion(message)
            variables.sesion[user_id] = votacion

        @bot.callback_query_handler(func=lambda call: True)
        def responder(message):
            user_id = message.from_user.id
            votacion = variables.sesion[user_id]
            votacion.responder_pregunta(message)


        @bot.message_handler(commands=['misvotaciones'])
        def mis_votaciones(message):
            user_id = message.from_user.id
            votaciones = utils.get_votaciones(user_id)
            text = '*Mis votaciones:*\n'
            for votacion in votaciones:
                text += '\n🔹 %s /votacion\_%d' % (votacion[0], votacion[3])
            bot.reply_to(message, text, parse_mode='Markdown')

        @bot.message_handler(regexp='^(/votacion_)\d+')
        def info_votacion(message):
            chat_id = message.chat.id
            try:
                votacion_id = message.text.split('_')[1]
                votacion = utils.get_votacion(votacion_id)
                if int(votacion[1]) != chat_id:
                    bot.send_message(chat_id, 'No tienes permiso para ver esta votación')
                else:
                    bot.send_message(chat_id, votacion)
            except Exception as e:
                bot.send_message(chat_id, 'Algo no fue bien')

        @bot.message_handler(commands=['compartir'])
        def compartir_votaciones(message):
            user_id = message.from_user.id
            votaciones = utils.get_votaciones(user_id)
            markup = types.InlineKeyboardMarkup()
            for votacion in votaciones:
                markup.add(types.InlineKeyboardButton(votacion[0], switch_inline_query="compartir"))
            bot.send_message(message.chat.id, "Mis votaciones", reply_markup=markup)


        bot.polling(none_stop=True)

    except Exception as e:
        print('Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
