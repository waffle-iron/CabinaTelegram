# -*- encoding: utf-8 -*-

import telebot
import configparser
import time

config = configparser.ConfigParser()
config.read('config.ini')
token_id = config['Telegram']['token_id']

bot = telebot.TeleBot(token_id)

admin_id = 14069151

while True:
    try:

        @bot.message_handler(commands=['help', 'start'])
        def send_welcome(message):
            bot.reply_to(message, 'Welcome!!')


        @bot.message_handler(commands=['cancel'])
        def cancel(message):
            chat_id = message.chat.id
            msg = bot.send_message(chat_id, 'Mira macho...')


        @bot.message_handler(commands=['encuesta'])
        def nombrar_encuesta(message):
            chat_id = message.chat.id
            msg = bot.send_message(chat_id, 'Introduzca el nombre de la encuesta')
            bot.register_next_step_handler(msg, crear_encuesta)


        def crear_encuesta(message):
            if message.text == '/cancel':
                return False
            nombreEncuesta = message
            # Crear encuesta en BD
            msg = bot.send_message(message.chat.id, 'Introduzca el numero de opciones (escriba /cancel para cancelar)')
            bot.register_next_step_handler(msg, crear_preguntas)


        def crear_preguntas(message):
            if message.text == '/cancel':
                return False
            num_preguntas = int(message.text)
            i = 0
            for i in range(num_preguntas):
                msg = bot.send_message(message.chat.id, 'Introduzca la respuestas')
                bot.register_next_step_handler(msg, almacenar_pregunta)
            # Crear encuesta en BD
            msg = bot.send_message(message.chat.id,
                                   '¿Desea crear otra encuesta?\nEn caso afirmativo escríbalo (escriba /cancel para salir)')
            bot.register_next_step_handler(msg, crear_encuesta())


        def almacenar_pregunta(message):
            if message.text == '/cancel':
                return False
            nombrePregunta = message
            # Crear pregunta en BD

    except Exception as e:
        print('Error: %s\nReiniciando en 10 seg' % e)
        time.sleep(10)
