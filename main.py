import asyncio
import os

import logging
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.user_handlers import register_user_handlers
from bot.midleware.middleware import register_middleware
from bot.data.alchemy.DDL import create_all_db_structure
from bot.data.alchemy.DML import insert_text_string


def register_handler(dp: Dispatcher) -> None:
    """
    Register user handlers in the dispatcher object.
    :param dp:
    :return:
    """
    register_user_handlers(dp=dp)


def register_bot_middleware(dp: Dispatcher) -> None:
    """
    Registering the middleware in the dispatcher object.
    :param dp:
    :return:
    """
    register_middleware(dp=dp)


def db_text_string_insert() -> None:
    """
    Writing text variables to the database.
    :return:
    """
    # insert_text_string(string_name=, string_text=, string_type="handlers", string_language="RU")
    insert_text_string(string_name="MORE_INFO", string_text="MORE INFO", string_type="handlers", string_language="RU")
    insert_text_string(string_name="GET_MORE_INFO", string_text="Тут больше информации!", string_type="handlers",
                       string_language="RU")
    insert_text_string(string_name="MSG_HI", string_text="Привет {}!", string_type="handlers", string_language="RU")
    insert_text_string(string_name="MSG_HI_AGAIN",
                       string_text="Привет {}! Мы уже знакомы, последний раз ты заходил {}.", string_type="handlers",
                       string_language="RU")


def create_rotating_log(path: str) -> None:
    """
    Log management function
    :param path:
    :return:
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(filename=path, mode="w", maxBytes=10000000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))

    logger.addHandler(file_handler)

    logging.debug('DEBUG MESSAGE')
    logging.info('INFO MESSAGE')
    logging.warning('WARNING MESSAGE')
    logging.error("ERROR MESSAGE")
    logging.critical("CRITICAL MESSAGE")


async def main() -> None:
    """
    Entry point
    :return:
    """

    token = os.getenv(key="TELEGRAM_API_TOKEN")

    bot = Bot(token=token)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    register_handler(dp=dp)
    register_bot_middleware(dp=dp)

    try:
        await dp.start_polling(reset_webhook=True)
    except Exception as _exc:
        logging.exception(_exc)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        log_path = os.path.abspath(os.path.join("", "bot", "logs", "bot_logs.log"))
        create_rotating_log(log_path)

        load_dotenv(dotenv_path=".env")
        create_all_db_structure(db_user_name=os.getenv(key="DB_USER_NAME"),
                                db_user_password=os.getenv(key="DB_USER_PASSWORD"),
                                db_address=os.getenv(key="DB_ADDRESS"),
                                db_name=os.getenv(key="DB_NAME"))
        # USE FOR SQLITE
        # create_all_db_structure(None, None, None, None)
        db_text_string_insert()
    except Exception as exc:
        logging.exception(exc)

    try:
        logging.warning(msg="BOT STARTED....")
        asyncio.run(main=main())
    except (KeyboardInterrupt, SystemExit):
        logging.warning("BOT STOPPED...")
