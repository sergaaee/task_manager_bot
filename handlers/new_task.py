from settings import dp, bot
from aiogram import types
from database import Database, Tasks
from aiogram_calendar import simple_cal_handler
from states import TaskForm
from aiogram.dispatcher import FSMContext


# new task
@dp.callback_query_handler(lambda c: c.data == 'nt')
async def new_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "nt"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await simple_cal_handler(callback_query.from_user.id)


@dp.message_handler(state=TaskForm.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await TaskForm.stime.set()
    await message.answer("When starts?")


@dp.message_handler(state=TaskForm.stime)
async def get_start_time(message: types.Message, state: FSMContext):
    try:
        if message.text.find(":") == -1 \
                or message.text.__len__() > 5 \
                or int(message.text[:2]) > 24 \
                or int(message.text[:2]) < 0 \
                or int(message.text[3:]) > 60 \
                or int(message.text[3:]) < 0:
            await message.answer(f"Incorrect time ❌\n"
                                 f"please enter in format: HH:MM")
        else:
            await state.update_data(stime=message.text)
            await TaskForm.etime.set()
            await message.answer("When ends?")
    except ValueError:
        await message.answer(f"Incorrect time ❌\n"
                             f"please enter in format: HH:MM")


@dp.message_handler(state=TaskForm.etime)
async def get_end_time(message: types.Message, state: FSMContext):
    try:
        if message.text.find(":") == -1 \
                or message.text.__len__() > 5 \
                or int(message.text[:2]) > 24 \
                or int(message.text[:2]) < 0 \
                or int(message.text[3:]) > 60 \
                or int(message.text[3:]) < 0:
            await message.answer(f"Incorrect time ❌\n"
                                 f"please enter in format: HH:MM")
        else:
            await state.update_data(etime=message.text)
            await TaskForm.desc.set()
            await message.answer("Description:")
    except ValueError:
        await message.answer(f"Incorrect time ❌\n"
                             f"please enter in format: HH:MM")


@dp.message_handler(state=TaskForm.desc)
async def get_desc(message: types.Message, state: FSMContext):
    await state.update_data(desc=message.text)
    data = await state.get_data()
    await state.finish()
    time_zone = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["time_zone"])[0]
    start_hour = data['stime'][:data['stime'].find(":")]
    start_minutes = data['stime'][data['stime'].find(":") + 1:]
    start_w_tz = int(start_hour) - int(time_zone)
    if int(start_w_tz) < 10:
        if int(start_minutes) < 10 and "0" not in start_minutes:
            start_time = f"0{start_w_tz}:0{start_minutes}"
        else:
            start_time = f"0{start_w_tz}:{start_minutes}"
    else:
        if int(start_minutes) < 10 and "0" not in start_minutes:
            start_time = f"{start_w_tz}:0{start_minutes}"
        else:
            start_time = f"{start_w_tz}:{start_minutes}"
    end_hour = data['etime'][:data['etime'].find(":")]
    end_minutes = data['etime'][data['etime'].find(":") + 1:]
    end_w_tz = int(end_hour) - int(time_zone)
    if int(end_w_tz) < 10:
        if int(end_minutes) < 10 and "0" not in end_minutes:
            end_time = f"0{end_w_tz}:0{end_minutes}"
        else:
            end_time = f"0{end_w_tz}:{end_minutes}"
    else:
        if int(end_minutes) < 10 and "0" not in end_minutes:
            end_time = f"{end_w_tz}:0{end_minutes}"
        else:
            end_time = f"{end_w_tz}:{end_minutes}"
    date = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["selected_date"])[0]
    Tasks().addt(name=data['name'], start_time=start_time, end_time=end_time, user_id=message.from_user.id,
                 desc=data['desc'], date=date)
    await message.answer("Successfully added ✅")
