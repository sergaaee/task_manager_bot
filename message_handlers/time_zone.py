from bot import dp
from states import TimeZoneForm
from aiogram import types
from aiogram.dispatcher import FSMContext
from database.database import Database


# setting up time zone
@dp.message_handler(commands=["timezone", "tz"])
async def ask_time_zone(message: types.Message):
    await message.answer(f"Okay, let's set up your time zone\n"
                         f"I need it for send you notification when time's up for your tasks\n"
                         f"Just send me in format from UTC\n"
                         f"Example: if you from Israel send +3\n"
                         f"if you from Brazil send -3")
    await TimeZoneForm.zone.set()


@dp.message_handler(state=TimeZoneForm.zone)
async def set_time_zone(message: types.Message, state: FSMContext):
    try:
        user_zone = float(message.text)
        if 15 > user_zone > -13:
            await state.update_data(zone=message.text)
            Database().update(table_name="Users", columns={"time_zone": user_zone}, id=message.from_user.id)
            await state.finish()
            await message.answer(f"You successfully set your time zone up ✅\n\n"
                                 f"Now you are ready-to-go\n"
                                 f"Just type /t and enjoy! 😉")
        else:
            await message.answer(f"Time zone {message.text} is incorrect ❌\n"
                                 f"Time zone should be from -12 to +14 🤕")
            await state.finish()
            await TimeZoneForm.zone.set()
    except ValueError:
        await message.answer(f"Time zone {message.text} is incorrect ❌\n"
                             f"Please send time zone in correct format 🤕")
        await state.finish()
        await TimeZoneForm.zone.set()
