from aiogram import types, Dispatcher
from bot.keyboards.user_keyboards import get_main_keyboard


async def cmd_start(msg: types.Message) -> None:
    """
    Start message handler
    :param msg:
    :return:
    """
    await msg.answer(text="Hello {}!".format(msg.from_user.first_name),
                     reply_markup=get_main_keyboard())


def register_user_handlers(dp: Dispatcher) -> None:
    """
    Register user handlers
    :param dp:
    :return:
    """
    dp.register_message_handler(cmd_start, commands=["start"])