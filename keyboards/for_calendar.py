from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# dialog calendar usage
ib_y = InlineKeyboardButton(text="✅", callback_data="y")
ib_n = InlineKeyboardButton(text="❌", callback_data="n")
ikb_agree = InlineKeyboardMarkup().add(ib_y, ib_n)
