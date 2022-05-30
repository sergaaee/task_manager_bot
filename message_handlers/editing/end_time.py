# end time editing
from bot import bot, dp
from database.database import Database
from states import EditForm
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == 'etime', state=[EditForm.name, EditForm.new_etime])
async def new_etime(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new end time:")
    await EditForm.new_etime.set()


@dp.message_handler(state=EditForm.new_etime)
async def edit_etime(message: types.Message, state: FSMContext):
    if message.text.find(":") == -1:
        await message.answer(f"Incorrect time ❌\n"
                             f"please enter in format: HH:MM")
    else:
        await state.update_data(new_etime=message.text)
        data = await state.get_data()
        time_zone = Database().select(table_name="Users", fetchone=True, id=message.from_user.id, columns=["time_zone"])[0]
        end_hour = data['new_etime'][:data['new_etime'].find(":")]
        end_minutes = data['new_etime'][data['new_etime'].find(":")+1:]
        end_w_tz = int(end_hour) - int(time_zone)
        if int(end_w_tz) < 10:
            if int(end_minutes) < 10:
                end_time = f"0{end_w_tz}:0{end_minutes}"
            else:
                end_time = f"0{end_w_tz}:{end_minutes}"
        else:
            if int(end_minutes) < 10:
                end_time = f"{end_w_tz}:0{end_minutes}"
            else:
                end_time = f"{end_w_tz}:{end_minutes}"
        Database().update(table_name="Tasks", columns={"end_time": end_time}, user_id=message.from_user.id,
                          name=data["name"])
        await state.finish()
        await message.answer("End time successfully edited ✅")