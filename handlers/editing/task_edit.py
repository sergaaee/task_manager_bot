# edit task
from settings import dp, bot
from database import Database
from aiogram import types
from states import EditForm
from aiogram.dispatcher import FSMContext
from keyboards import params_keyboard


@dp.callback_query_handler(lambda c: c.data == "et")
async def ed_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "et"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    from aiogram_calendar import simple_cal_handler
    await simple_cal_handler(callback_query.from_user.id)


async def edit_task(callback_query):
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    names = Database().select(table_name="Tasks", user_id=callback_query.from_user.id, columns=["name"], date=date)
    if len(names) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date.")
        return
    res = "\n\n".join([i[0] for i in names])
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Send task's name that you want to edit:\n\n{res}")
    await EditForm.name.set()


@dp.message_handler(state=EditForm.name)
async def get_name_for_edit(message: types.Message, state: FSMContext):
    global check
    try:
        check = Database().select(table_name="Tasks", user_id=message.from_user.id, fetchone=True, name=message.text, columns=["name"])[0]
        await state.update_data(name=message.text)
        await message.answer("Choose what you want to edit:", reply_markup=params_keyboard)
    except TypeError:
        await message.answer("Wrong name ❌\ntry one more time")
        await state.finish()
        await edit_task(callback_query=message)
