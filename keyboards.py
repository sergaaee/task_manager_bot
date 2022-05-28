from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# choose menu
ib_nt = InlineKeyboardButton("Add task", callback_data="nt")
ib_st = InlineKeyboardButton("Show tasks", callback_data="st")
ib_dt = InlineKeyboardButton("Delete task", callback_data="dt")
ib_et = InlineKeyboardButton("Edit task", callback_data="et")
inline_kb_choose = InlineKeyboardMarkup().add(ib_nt, ib_st, ib_dt, ib_et)


# params for editing
param_name = InlineKeyboardButton("name", callback_data="name")
param_stime = InlineKeyboardButton("start time", callback_data="stime")
param_etime = InlineKeyboardButton("end time", callback_data="etime")
param_desc = InlineKeyboardButton("description", callback_data="desc")
params_keyboard = InlineKeyboardMarkup().add(param_name, param_stime, param_etime, param_desc)


# dialog calendar usage
ib_y = InlineKeyboardButton(text="✅", callback_data="y")
ib_n = InlineKeyboardButton(text="❌", callback_data="n")
ikb_agree = InlineKeyboardMarkup().add(ib_y, ib_n)