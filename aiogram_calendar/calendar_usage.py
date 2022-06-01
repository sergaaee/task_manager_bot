from aiogram_calendar import DialogCalendar, dialog_cal_callback
from aiogram.types import CallbackQuery
from keyboards import ikb_agree
from settings import bot, dp
from aiogram import types
from database.db import Database
from states import TaskForm


# calendar
async def simple_cal_handler(user_id):
    await bot.send_message(text="Please select a date: ", chat_id=user_id,
                           reply_markup=await DialogCalendar().start_calendar())


@dp.callback_query_handler(lambda c: c.data == 'y')
async def y_agree(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    selected_command = Database().select(table_name="Users", fetchone=True, id=callback_query.from_user.id,
                                         columns=["selected_command"])[0]
    if selected_command == "nt":
        await bot.send_message(callback_query.from_user.id, text="Enter name of a task:")
        await TaskForm.name.set()
    elif selected_command == "st":
        from handlers import show_tasks
        await show_tasks(callback_query=callback_query)
    elif selected_command == "dt":
        from handlers import delete_task
        await delete_task(callback_query=callback_query)
    elif selected_command == "et":
        from handlers import edit_task
        await edit_task(callback_query=callback_query)


@dp.callback_query_handler(lambda c: c.data == "n")
async def n_agree(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(text="You cancelled operation ✅", chat_id=callback_query.from_user.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.callback_query_handler(dialog_cal_callback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: dict):
    selected, date = await DialogCalendar().process_selection(callback_query, callback_data)
    if selected:
        date = date.strftime("%d/%m/%Y")
        Database().update(table_name="Users", columns={"selected_date": date}, id=callback_query.from_user.id)
        await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        await callback_query.message.answer(
            f'You selected {date},\nAre you sure?',
            reply_markup=ikb_agree,
        )