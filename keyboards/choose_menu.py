from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# choose menu
ib_nt = InlineKeyboardButton("Add task", callback_data="nt")
ib_st = InlineKeyboardButton("Show tasks", callback_data="st")
ib_dt = InlineKeyboardButton("Delete task", callback_data="dt")
ib_et = InlineKeyboardButton("Edit task", callback_data="et")
inline_kb_choose = InlineKeyboardMarkup().add(ib_nt, ib_st, ib_dt, ib_et)
