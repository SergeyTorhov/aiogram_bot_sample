from aiogram import types, Dispatcher
from bot.keyboards.user_keyboards import get_main_keyboard
from datetime import datetime

from bot.database.alchemy.DML import find_userdata_by_id, create_new_user, update_user_data


async def cmd_start(msg: types.Message) -> None:
    """
    Start message handler
    :param msg:
    :return:
    """

    user_data = find_userdata_by_id(msg.from_user.id)
    text = "Привет {}!".format(msg.from_user.first_name)

    if not user_data:
        create_new_user(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                        first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)
    else:
        text = "Привет {}! Мы уже знакомы, последний раз ты заходил {}." \
            .format(msg.from_user.first_name,
                    datetime.strftime(user_data[1], '%Y-%m-%d %H:%M:%S'))
        update_user_data(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                         first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)

    await msg.answer(text=text, reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    """
    Register user handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(cmd_start, commands=["start"])
