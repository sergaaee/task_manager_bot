import time
import settings
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup
from aiogram.utils import executor
import keyboard as kb
from state import TaskForm

storage = MemoryStorage()
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot, storage=storage)




@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(fio=name)
    await TaskForm.stime.set()


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    stime = message.text
    await state.set_data(stime=stime)
    await TaskForm.etime.set()


@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    etime = message.text
    await state.set_data(etime=etime)
    await TaskForm.desc.set()


@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    desc = message.text
    data = await state.get_data()
    await state.finish()

    print(data)




@dp.message_handler(commands=['start'])
async def cmd_start(message: Message):
    await message.answer('Pick a calendar', reply_markup=await kb.SimpleCalendar.start_calendar())


@dp.callback_query_handler(kb.SimpleCalendar.simple_callback().filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await kb.SimpleCalendar.process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(f'You selected {date.strftime("%d/%m/%Y")}')


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)

    executor.start_polling(dp, skip_updates=True)
