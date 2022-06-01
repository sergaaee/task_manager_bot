from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# params for editing
param_name = InlineKeyboardButton("name", callback_data="name")
param_stime = InlineKeyboardButton("start time", callback_data="stime")
param_etime = InlineKeyboardButton("end time", callback_data="etime")
param_desc = InlineKeyboardButton("description", callback_data="desc")
params_keyboard = InlineKeyboardMarkup().add(param_name, param_stime, param_etime, param_desc)