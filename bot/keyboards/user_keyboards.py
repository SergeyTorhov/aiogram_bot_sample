from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard() -> InlineKeyboardMarkup:
    """
    Get keyboard for user main menu
    :return:
    """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="MORE INFO", callback_data="cb_btn_more_info")]
    ])
    return ikb
