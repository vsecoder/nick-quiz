from .text import text_handler
from .start import start_handler

from telebot.async_telebot import AsyncTeleBot


def init_handlers(bot: AsyncTeleBot):
    bot.register_message_handler(start_handler, commands=['start'], pass_bot=True)
    bot.register_message_handler(text_handler, content_types=['text'], pass_bot=True)
