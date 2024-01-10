import asyncio
import logging
from telebot.async_telebot import AsyncTeleBot

from app import db
from app.db import close_orm, init_orm
from app.handlers import init_handlers

from app.config import Config

bot = AsyncTeleBot(Config.token)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    init_handlers(bot)

    tortoise_config = {
        "connections": {
            "default": "sqlite://db.sqlite3"
        },
        "apps": {
            "models": {
                "models": ["app.db.functions", "aerich.models"],
                "default_connection": "default",
            }
        }
    }

    try:
        await db.create_models(tortoise_config)
    except FileExistsError:
        await db.migrate_models(tortoise_config)

    await init_orm(tortoise_config)
    logger.info("Bot started.")
    await bot.polling()


if __name__ == '__main__':
    asyncio.run(main())
    asyncio.run(close_orm())
