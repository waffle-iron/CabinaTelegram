# -*- encoding: utf-8 -*-

import telebot
from telebot import types

import variables
from src.utils import Utils

utils = Utils()

bot = variables.bot

class Votacion:
    def __init__(self):
        self.titulo = ""
        self.preguntas_respuestas = {}
        self.respuestas_seleccionadas = []
        self.owner_id = 0

    def crear_votacion(self, message):
        self.pide_titulo(message.chat.id)
        self.owner_id = message.from_user.id

    def pide_titulo(self, chat_id):
        msg = bot.send_message(chat_id, 'Dime un *título* para la votación:', parse_mode='Markdown')
        bot.register_next_step_handler(msg, self.captura_titulo)

    def captura_titulo(self, message):
        titulo = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(titulo):
            bot.send_message(message.chat.id, '❌ Votación cancelada')
            return False
        else:
            self.titulo = titulo
            self.pide_pregunta(chat_id)

    def pide_pregunta(self, chat_id):
        if self.get_num_preguntas() == 0:
            text = '❔Dime tu primera *pregunta:*'
        else:
            text = '❔Siguiente *pregunta:* \n\nPara terminar escribe /done o simplemente pulsa sobre el enlace.'
        msg = bot.send_message(chat_id, text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, self.captura_pregunta)

    def captura_pregunta(self, message):
        pregunta = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(pregunta):
            command = telebot.util.extract_command(pregunta)
            if command == 'done' and self.get_num_preguntas() >= 1:
                utils.almacenar_votacion(self.titulo, self.owner_id, self.preguntas_respuestas)
                bot.send_message(chat_id, '✅ Encuesta creada con éxito')
                bot.send_message(chat_id, str(self.to_string()), parse_mode='Markdown')
                # Prueba para comprobar que funciona el metodo de enviar pregunta
                self.enviar_pregunta(chat_id)
            elif command == 'done':
                bot.send_message(chat_id, 'Necesitas al menos una pregunta para crear la votación.')
                self.pide_pregunta(chat_id)
            else:
                bot.send_message(chat_id, '❌ Votación cancelada')
                return False
        else:
            self.añade_pregunta(pregunta)
            self.pide_respuesta(message.chat.id)

    def pide_respuesta(self, chat_id):
        if self.get_num_respuestas() == 0:
            text = '✏️ Dime una *respuesta:*'
        elif self.get_num_respuestas() == 1:
            text = '✏️ Dime otra *respuesta:*'
        else:
            text = '✏️ Dime otra *respuesta:* \n\nPara pasar a la siguiente pregunta escribe /done' \
                   ' o simplemente pulsa sobre el enlace.'

        msg = bot.send_message(chat_id, text, parse_mode='Markdown')
        bot.register_next_step_handler(msg, self.captura_respuesta)

    def captura_respuesta(self, message):
        respuesta = message.text
        chat_id = message.chat.id

        if telebot.util.is_command(respuesta):
            command = telebot.util.extract_command(respuesta)
            if command == 'done' and self.get_num_respuestas() >= 2:
                self.pide_pregunta(chat_id)
            elif command == 'done':
                bot.send_message(chat_id, 'Necesitas al menos dos respuestas para la pregunta.')
                self.pide_respuesta(chat_id)
            else:
                bot.send_message(chat_id, '❌ Votación cancelada')
                return False
        else:
            self.añade_respuesta(respuesta)
            self.pide_respuesta(chat_id)

    def mostrar_preguntas(self):
        return sorted(self.preguntas_respuestas)

    def mostrar_respuestas(self, pregunta):
        return self.preguntas_respuestas[pregunta]

    def añade_pregunta(self, pregunta):
        num_preguntas = len(self.preguntas_respuestas)
        self.preguntas_respuestas['%d. %s' % (num_preguntas+1, pregunta)] = []

    def añade_respuesta(self, respuesta):
        pregunta = sorted(self.preguntas_respuestas)[-1]
        self.preguntas_respuestas[pregunta].append(respuesta)

    def get_num_preguntas(self):
        return len(self.preguntas_respuestas)

    def get_num_respuestas(self):
        pregunta = sorted(self.preguntas_respuestas)[-1]
        return len(self.preguntas_respuestas[pregunta])

    def enviar_pregunta(self, chat_id):
        global msg_question_id, preguntas
        if 'preguntas' not in globals():
            preguntas = self.mostrar_preguntas()
            preguntas.reverse()
        if len(preguntas) == 0:
            bot.edit_message_text('👍 Gracias por su participación', chat_id=chat_id, message_id=msg_question_id)
            del msg_question_id, preguntas
            return False
        pregunta = preguntas.pop()
        respuestas = self.mostrar_respuestas(pregunta)
        markup = types.InlineKeyboardMarkup()
        for respuesta in respuestas:
            markup.add(types.InlineKeyboardButton(respuesta, callback_data=respuesta))
        if 'msg_question_id' not in globals():
            msg_question = bot.send_message(chat_id, pregunta, reply_markup=markup)
            msg_question_id = msg_question.message_id
        else:
            bot.edit_message_text(pregunta, chat_id=chat_id, message_id=msg_question_id)
            bot.edit_message_reply_markup(chat_id=chat_id, message_id=msg_question_id, reply_markup=markup)

    def responder_pregunta(self, message):
        chat_id = message.message.chat.id
        respuesta = message.data
        self.respuestas_seleccionadas.append(respuesta)
        self.enviar_pregunta(chat_id)

    def to_string(self):
        text = '*%s*\n\n' % self.titulo
        for pregunta in sorted(self.preguntas_respuestas):
            text += '%s\n' % pregunta
            for respuesta in self.preguntas_respuestas[pregunta]:
                text += '    ▫️ %s\n' % respuesta

        return text
