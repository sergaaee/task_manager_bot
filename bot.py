import time

from database import Users, Tasks
from settings import token
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext


# Initialize bot and dispatcher
bot = Bot(token=token)
dp = Dispatcher(bot)

class Task(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username, )
    await message.answer('hello message')





if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)