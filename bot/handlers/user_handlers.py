from aiogram import types, Dispatcher

from datetime import datetime

from bot.data.alchemy.DML import find_userdata_by_id, create_new_user, update_user_data, find_text_string
from bot.keyboards.user_keyboards import get_main_keyboard
from bot.midleware.middleware import rate_limit

import logging


@rate_limit(limit=60, key="start")
async def cmd_start(msg: types.Message) -> None:
    """
    Start message handler.
    :param msg:
    :return:
    """
    try:
        user_data = find_userdata_by_id(msg.from_user.id)
        text = find_text_string(string_name="MSG_HI").format(msg.from_user.first_name)

        if not user_data:
            create_new_user(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                            first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)
        else:
            text = find_text_string(string_name="MSG_HI_AGAIN").format(msg.from_user.first_name,
                                                                       datetime.strftime(user_data[1],
                                                                                         '%Y-%m-%d %H:%M:%S'))
            update_user_data(user_id=msg.from_user.id, last_call=datetime.now(), user_name=msg.from_user.username,
                             first_name=msg.from_user.first_name, last_name=msg.from_user.last_name)

        await msg.answer(text=text, reply_markup=get_main_keyboard())
    except Exception as exc:
        logging.exception(msg=exc)


@rate_limit(limit=15, key="cb_btn_more_info")
async def ikb_more_info(cb: types.callback_query):
    """
    Callback handler
    :param cb:
    :return:
    """
    try:
        if cb.data == "cb_btn_more_info":
            await cb.answer(find_text_string(string_name="GET_MORE_INFO"))
    except Exception as exc:
        logging.exception(msg=exc)


def register_user_handlers(dp: Dispatcher) -> None:
    """
    Register user handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_callback_query_handler(callback=ikb_more_info)
