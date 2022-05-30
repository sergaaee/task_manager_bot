from asyncio import create_task, sleep
from bot import bot
from database.database import Tasks, Database


# notifications
async def user_list():
    """background task which is created when bot starts"""

    while True:
        await sleep(60)
        start_time, users = Tasks().notification()
        if len(users) == 0:
            continue
        else:
            for user_id in users[0]:
                info = Database().select(table_name="Tasks", fetchone=False, user_id=user_id, start_time=start_time, columns=["name", "end_time", "desc"])
                to_send = f"Your task begins:\n\nname: {info[0][0]}\nends at: {info[0][1]}\ndescription: {info[0][2]}"
                await bot.send_message(chat_id=user_id, text=to_send)


async def start_check():
    """List of actions which should be done before bot start"""
    create_task(user_list())  # creates background task
