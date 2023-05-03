import asyncio
import os

from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types

from bot.handlers.user_handlers import register_user_handlers


def register_handler(dp: Dispatcher) -> None:
    register_user_handlers(dp=dp)


def on_startup() -> None:
    print("Bot starting...")


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


if __name__ == "__main__":
    asyncio.run(main=main())
