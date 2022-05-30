# edit task
from bot import bot, dp
from database.database import Database
from message_handlers.calendar import simple_cal_handler as ____simple_cal_handler
from states import EditForm
from aiogram import types


@dp.callback_query_handler(lambda c: c.data == "et")
async def ed_task(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "et"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await ____simple_cal_handler(callback_query.from_user.id)


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
