from bot import dp
from aiogram import types
from database.database import Users


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    await message.answer(f"Hello 👋\n\nI'm a bot that will help you to plan your day 😊\n"
                         f"With me you can easily add, watch, delete, edit tasks that you have to do!"
                         f"\n\nJust send /tz and you will figure out with me 🎯")
    