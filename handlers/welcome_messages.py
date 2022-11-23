from settings import dp
from database import Users
from aiogram import types


@dp.message_handler(commands=['start', 's', 'help', 'h'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    time_zone = Users().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["time_zone"])[0]
    if time_zone == "None":
        await message.answer(f"Hello 👋\n\nI'm a bot that will help you to plan your day 😊\n"
                             f"With me you can easily add, watch, delete, edit tasks that you have to do!"
                             f"\n\nJust send /tz and you will figure out with me 🎯")
    else:
        await message.answer(f"If you want to proceed to main menu send /t \n"
                             f"If you need to change your timezone type /tz")
