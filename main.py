import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from bot.handlers.user_handlers import register_user_handlers
from bot.database.alchemy.DDL import create_all_db_structure


def register_handler(dp: Dispatcher) -> None:
    register_user_handlers(dp=dp)


async def main() -> None:
    """
    Entry point
    :return:
    """
    load_dotenv(dotenv_path=".env")
    token = os.getenv(key="TELEGRAM_API_TOKEN")

    bot = Bot(token=token)
    dp = Dispatcher(bot=bot)
    register_handler(dp=dp)

    try:
        on_startup()
        await dp.start_polling()
    except Exception as exc:
        print("Exception: {}".format(exc))


def on_startup() -> None:
    create_all_db_structure()
    print("Bot starting...")


if __name__ == "__main__":
    asyncio.run(main=main())
