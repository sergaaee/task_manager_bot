# name editing
from database.database import Database
from message_handlers.editing.edit_task import edit_task
from states import EditForm
from keyboards import params_keyboard
from aiogram.dispatcher import FSMContext
from bot import bot, dp
from aiogram import types


@dp.message_handler(state=EditForm.name)
async def get_name(message: types.Message, state: FSMContext):
    global check
    try:
        check = Database().select(table_name="Tasks", user_id=message.from_user.id, fetchone=True, name=message.text, columns=["name"])[0]
        await state.update_data(name=message.text)
        await message.answer("Choose what you want to edit:", reply_markup=params_keyboard)
    except TypeError:
        await message.answer("Wrong name ❌\ntry one more time")
        await state.finish()
        await edit_task(callback_query=message)


@dp.callback_query_handler(lambda c: c.data == 'name', state=[EditForm.name, EditForm.new_name])
async def new_name(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new name:")
    await EditForm.new_name.set()


@dp.message_handler(state=EditForm.new_name)
async def edit_name(message: types.Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"name": data["new_name"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("Name successfully edited ✅")
