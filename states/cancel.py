from settings import dp, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types


# cancel any state
@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no state to cancel ❌")
        return
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("You cancelled operation ✅")
    await state.finish()