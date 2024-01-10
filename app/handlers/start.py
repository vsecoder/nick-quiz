from telebot.async_telebot import AsyncTeleBot
from telebot import types

from app.db.functions import User

import logging

logger = logging.getLogger(__name__)


async def start_handler(message: types.Message, bot: AsyncTeleBot):
    """/start command handler"""
    user_id = message.from_user.id
    user = await User.is_registered(user_id)

    text = (
        "✨ <b>Привет, в этом боте ты можешь пройти квиз про программиста и ИИ!</b>\n"
        "<u>Напиши что-нибудь в чат, что бы начать)))</u>\n\n"
    )

    if not user:
        await User.register(user_id)
        logger.info(f"New user #{user_id}")

    await bot.send_message(message.chat.id, text, parse_mode="HTML")
