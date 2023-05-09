import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.user_handlers import register_user_handlers
from bot.midleware.middleware import register_middleware
from bot.data.alchemy.DDL import create_all_db_structure


def register_handler(dp: Dispatcher) -> None:
    register_user_handlers(dp=dp)


def register_bot_middleware(dp: Dispatcher) -> None:
    register_middleware(dp=dp)


async def main() -> None:
    """
    Entry point
    :return:
    """
    load_dotenv(dotenv_path=".env")
    token = os.getenv(key="TELEGRAM_API_TOKEN")

    bot = Bot(token=token)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    register_handler(dp=dp)
    register_bot_middleware(dp=dp)

    try:
        on_startup()
        await dp.start_polling(reset_webhook=True)
    except Exception as exc:
        print("Exception: {}".format(exc))


def on_startup() -> None:
    create_all_db_structure(db_user_name=os.getenv(key="DB_USER_NAME"),
                            db_user_password=os.getenv(key="DB_USER_PASSWORD"),
                            db_address=os.getenv(key="DB_ADDRESS"),
                            db_name=os.getenv(key="DB_NAME"))
    # create_all_db_structure(None, None, None, None)
    print("Bot starting...")


if __name__ == "__main__":
    asyncio.run(main=main())
