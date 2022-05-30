from bot import bot, dp
from database.database import Database, Tasks
from message_handlers.calendar import simple_cal_handler as _simple_cal_handler
from aiogram import types


# show tasks
@dp.callback_query_handler(lambda c: c.data == "st")
async def find_tasks(callback_query: types.CallbackQuery):
    Database().update(table_name="Users", columns={"selected_command": "st"}, id=callback_query.from_user.id)
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await _simple_cal_handler(user_id=callback_query.from_user.id)


async def show_tasks(callback_query):
    date = \
        Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                          columns=["selected_date"])[0]
    data = Tasks().showt(user_id=callback_query.from_user.id, date=date)
    result = []
    for each in data:
        result.append("name: " + each[0] + ",\nstarts at: " + each[1] + ",\nends at: " + each[2] + ",\n" + each[3])
    if len(result) == 0:
        await bot.send_message(chat_id=callback_query.from_user.id, text="You have no tasks for selected date ❌")
        return
    else:
        for i in result:
            await bot.send_message(chat_id=callback_query.from_user.id, text=i)
