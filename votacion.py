# -*- encoding: utf-8 -*-

import variables
import telebot

bot = variables.bot

class Votacion:
    def __init__(self):
        self.titulo = ""
        self.preguntas_respuestas = {}

    def crear_votacion(self, message):
        self.pide_titulo(message.chat.id)

    def pide_titulo(self, chat_id):
        msg = bot.send_message(chat_id, '¿Qué título desea para la votación?')
        bot.register_next_step_handler(msg, self.captura_titulo)

    def captura_titulo(self, message):
        titulo = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(titulo):
            bot.send_message(message.chat.id, 'Votación cancelada')
            return False
        else:
            self.titulo = titulo
            self.pide_pregunta(chat_id)

    def pide_pregunta(self, chat_id):
        msg = bot.send_message(chat_id, 'Dime una pregunta, /done para terminar')
        bot.register_next_step_handler(msg, self.captura_pregunta)

    def captura_pregunta(self, message):
        pregunta = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(pregunta):
            command = telebot.util.extract_command(pregunta)
            if command == 'done':
                bot.send_message(chat_id, 'De acuerdo, encuesta creada')
                bot.send_message(chat_id, str(self.preguntas_respuestas))
            else:
                bot.send_message(chat_id, 'Votación cancelada')
                return False
        else:
            self.añade_pregunta(pregunta)
            self.pide_respuesta(message.chat.id)

    def pide_respuesta(self, chat_id):
        msg = bot.send_message(chat_id, 'Dime una respuesta, /done para terminar')
        bot.register_next_step_handler(msg, self.captura_respuesta)

    def captura_respuesta(self, message):
        respuesta = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(respuesta):
            command = telebot.util.extract_command(respuesta)
            if command == 'done':
                self.pide_pregunta(chat_id)
            else:
                bot.send_message(chat_id, 'Votación cancelada')
                return False
        else:
            self.añade_respuesta(respuesta)
            self.pide_respuesta(chat_id)

    def añade_pregunta(self, pregunta):
        num_preguntas = len(self.preguntas_respuestas)
        self.preguntas_respuestas['%d. %s' % (num_preguntas+1, pregunta)] = []

    def añade_respuesta(self, respuesta):
        pregunta = sorted(self.preguntas_respuestas)[-1]
        self.preguntas_respuestas[pregunta].append(respuesta)