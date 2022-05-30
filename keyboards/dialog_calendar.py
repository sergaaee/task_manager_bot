# dialog calendar usage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

ib_y = InlineKeyboardButton(text="✅", callback_data="y")
ib_n = InlineKeyboardButton(text="❌", callback_data="n")
ikb_agree = InlineKeyboardMarkup().add(ib_y, ib_n)
