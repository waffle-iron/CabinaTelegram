import telebot
import configparser

config = configparser.ConfigParser()
config.read('/home/jossalgon/Documentos/workspace/CabinaTelegram/src/config.ini')
token_id = config['Telegram']['token_id']

bot = telebot.TeleBot(token_id)

sesion = {}