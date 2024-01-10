from telebot.async_telebot import AsyncTeleBot
from telebot import types

from app.db.functions import User
from app.utils.twee import TweeReader
import logging

logger = logging.getLogger(__name__)

twee = TweeReader("quiz.twee")
formatted = twee.format()


async def text_handler(message: types.Message, bot: AsyncTeleBot):
    """all messages handler for quiz"""
    user = await User.is_registered(message.from_user.id)

    if not user:
        return await bot.send_message(message.chat.id, "Вы не зарегистрированы в боте! Напишите /start")

    scene = formatted['scenes'][formatted['data']['StoryData']['start']]

    if not user.step_title == 'start':
        try:
            last_scene = formatted['scenes'][user.step_title]
            link = [link for link in last_scene['links'] if link[0] == message.text][0]
            scene = formatted['scenes'][link[1]]
        except IndexError:
            pass  # if link not found, go to start scene

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for title, _ in scene['links']:
        keyboard.add(types.KeyboardButton(title))

    try:
        await bot.send_photo(
            message.chat.id,
            open(scene['image'], 'rb'),
            caption=scene['text'],
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except FileNotFoundError:
        await bot.send_message(message.chat.id, scene['text'], parse_mode="HTML", reply_markup=keyboard)
    await User.update(user, step_title=scene['title'])
