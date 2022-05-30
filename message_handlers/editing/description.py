# description editing
from database.database import Database
from states import EditForm
from bot import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == 'desc', state=[EditForm.name, EditForm.new_desc])
async def new_description(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id, text="Enter new description:")
    await EditForm.new_desc.set()


@dp.message_handler(state=EditForm.new_desc)
async def edit_description(message: types.Message, state: FSMContext):
    await state.update_data(new_desc=message.text)
    data = await state.get_data()
    Database().update(table_name="Tasks", columns={"desc": data["new_desc"]}, user_id=message.from_user.id,
                      name=data["name"])
    await state.finish()
    await message.answer("Description successfully edited ✅")
