from aiogram import types, Dispatcher
from bot.keyboards.user_keyboards import get_main_keyboard
from datetime import datetime

import os

# from bot.database.sqlite import BotDBFunction
from bot.database.alchemy.DML import AllDML


async def cmd_start(msg: types.Message) -> None:
    """
    Start message handler
    :param msg:
    :return:
    """
    sqlite_db_name = os.path.abspath(os.path.join("", "bot_sqlite_db"))
    tmp = AllDML(sqlite_db_name)

    user_data = tmp.find_user_by_id(msg.from_user.id)
    print(f"USER_DATA: {user_data}")

    text = "Привет {}!".format(msg.from_user.first_name)

    if not user_data:
        tmp.insert_user_data(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                             first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)
    else:
        text = "Привет {}! Мы уже знакомы, последний раз ты заходил {}.".format(msg.from_user.first_name,
                                                                                user_data.last_call)
        tmp.update_user_data(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                             first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)

    await msg.answer(text=text, reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    """
    Register user handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(cmd_start, commands=["start"])
