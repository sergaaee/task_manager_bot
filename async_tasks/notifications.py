# notifications

from asyncio import create_task, sleep
from database.db import Tasks, Database
from settings import bot, Dispatcher


# notifications
async def user_list():
    """background task which is created when bot starts"""

    while True:
        await sleep(1)
        start_time, users = Tasks().notification()
        if len(users) == 0:
            continue
        else:
            for user_id in users[0]:
                info = Database().select(table_name="Tasks", fetchone=False, user_id=user_id, start_time=start_time, columns=["name", "end_time", "desc"])
                time_zone = Database().select(table_name="Users", fetchone=True, id=user_id, columns=["time_zone"])[0]
                end_hour = info[0][1][:info[0][1].find(":")]
                end_minutes = info[0][1][info[0][1].find(":"):]
                end_time = f"{int(end_hour)+time_zone}{end_minutes}"
                to_send = f"Your task begins:\n\nname: {info[0][0]}\nends at: {end_time}\ndescription: {info[0][2]}"
                await bot.send_message(chat_id=user_id, text=to_send)


async def start_check(dispatcher: Dispatcher):
    """List of actions which should be done before bot start"""
    create_task(user_list())  # creates background task