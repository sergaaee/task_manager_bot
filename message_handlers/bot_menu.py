from aiogram import types
from database.database import Database
from bot import bot, dp
from keyboards import inline_kb_choose
from time_zone import ask_time_zone


# showing bot's menu
@dp.message_handler(commands=["t", "tasks"])
async def act_choosing(message: types.Message):
    if not Database().select(table_name="Users", columns="time_zone", id=message.from_user.id):
        await message.answer("I'm sorry, but I can't work with out knowledge of your time zone")
        await ask_time_zone(message)
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
        await message.answer("Choose what you want to do:", reply_markup=inline_kb_choose)
