from settings import bot, dp
from database import Database
from states import EditForm
from aiogram import types
from aiogram.dispatcher import FSMContext


# name editing
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
