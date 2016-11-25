# -*- encoding: utf-8 -*-

import variables

bot = variables.bot

class Votacion:
    def nombrar_votacion(self, message):
        chat_id = message.chat.id
        msg = bot.send_message(chat_id, 'Introduzca el nombre de la encuesta')
        bot.register_next_step_handler(msg, self.crear_encuesta)

    def crear_encuesta(self, message):
        if message.text == '/cancel':
            return False
        nombreEncuesta = message.text
        # Crear encuesta en BD
        msg = bot.send_message(message.chat.id, 'Introduzca el numero de opciones (escriba /cancel para cancelar)')
        bot.register_next_step_handler(msg, self.crear_preguntas)

    def crear_preguntas(self, message):
        if message.text == '/cancel':
            return False
        num_preguntas = int(message.text)
        for i in range(0, num_preguntas):
            msg = bot.send_message(message.chat.id, 'Introduzca la respuestas')
            bot.register_next_step_handler(msg, self.almacenar_pregunta)
        # Crear encuesta en BD
        msg = bot.send_message(message.chat.id,
                               '¿Desea crear otra encuesta?\nEn caso afirmativo escríbalo (escriba /cancel para salir)')
        bot.register_next_step_handler(msg, self.crear_encuesta())

    def almacenar_pregunta(self, message):
        if message.text == '/cancel':
            return False
        nombrePregunta = message
        # Crear pregunta en BD
