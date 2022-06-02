# delete task
from settings import dp, bot
from database import Database, Tasks
from states import DeleteForm
from aiogram import types
from aiogram.dispatcher import FSMContext


@dp.callback_query_handler(lambda c: c.data == "dt")
async def del_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "dt"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    from aiogram_calendar import simple_cal_handler
    await simple_cal_handler(callback_query.from_user.id)


async def delete_task(callback_query: types.CallbackQuery) -> ():
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    names = Database().select(table_name="Tasks", user_id=callback_query.from_user.id, columns=["name"], date=date)
    if len(names) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date.")
        return
    res = "\n\n".join([i[0] for i in names])
    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Send task's name that you want to delete:\n\n{res}",)
    await DeleteForm.name.set()

    @dp.message_handler(state=DeleteForm.name)
    async def get_del_name(message: types.Message, state: FSMContext):
        global check
        await state.update_data(name=message.text)
        try:
            check = Database().select(table_name="Tasks", user_id=message.from_user.id, fetchone=True, name=message.text,
                                      columns=["name"])[0]
            Tasks().delt(date=date, name=message.text)
            await state.finish()
            await message.answer("Successfully deleted ✅")
        except TypeError:
            await message.answer("Wrong name ❌\ntry one more time")
            await delete_task(message)
