from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.data.text_model import MORE_INFO


def get_main_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for user main menu
    :return:
    """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=MORE_INFO, callback_data="cb_btn_more_info")]
    ])
    return ikb
