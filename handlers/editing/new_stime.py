from settings import bot, dp
from states import EditForm
from aiogram import types
from aiogram.dispatcher import FSMContext
from database import Database


# start time editing
@dp.callback_query_handler(lambda c: c.data == 'stime', state=[EditForm.name, EditForm.new_stime])
async def new_stime(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new start time:")
    await EditForm.new_stime.set()


@dp.message_handler(state=EditForm.new_stime)
async def edit_stime(message: types.Message, state: FSMContext):
    if message.text.find(":") == -1:
        await message.answer(f"Incorrect time ❌\n"
                             f"please enter in format: HH:MM")
    else:
        await state.update_data(new_stime=message.text)
        data = await state.get_data()
        time_zone = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["time_zone"])[0]
        start_hour = data['new_stime'][:data['new_stime'].find(":")]
        start_minutes = data['new_stime'][data['new_stime'].find(":")+1:]
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
        Database().update(table_name="Tasks", columns={"start_time": start_time}, user_id=message.from_user.id,
                          name=data["name"])
        await state.finish()
        await message.answer("Start time successfully edited ✅")
