
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from database import Users, Tasks
from settings import token
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage = storage)

class TaskForm(StatesGroup):
    name = State()
    stime = State()
    etime = State()
    desc = State()


@dp.message_handler(commands=['start', 'help', 'h', 's'])
async def send_welcome(message: types.Message):
    Users().add(message.from_user.id, message.from_user.username)
    await message.answer('hello message')


@dp.message_handler(commands=['nt', 'new_task'])
async def start_date(message: types.Message):
    await TaskForm.name.set()
    await message.answer("Name your task:")


@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await TaskForm.stime.set()
    await message.answer("When task starts?")


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    stime = message.text
    await state.update_data(stime=stime)
    await TaskForm.etime.set()
    await message.answer("When task ends?")

@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    etime = message.text
    await state.update_data(etime=etime)
    await TaskForm.desc.set()
    await message.answer("Description:")

@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    desc = message.text
    await state.update_data(desc = desc)
    data = await state.get_data()
    await state.finish()

    Tasks().add(name=data['name'], user_id= message.from_user.id, start_time=data['stime'], end_time=data['etime'], desc=data['desc'],)
    await message.answer("Success!")


if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    # bot start
    executor.start_polling(dp, skip_updates=True)
