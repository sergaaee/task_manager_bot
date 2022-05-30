# cancel any state
from bot import dp, bot
import logging
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


@dp.message_handler(state="*", commands="cancel")
@dp.message_handler(Text(equals="cancel", ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("There is no state to cancel ❌")
        return
    logging.info('Cancelling state %r', current_state)
    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer("You cancelled operation ✅")
    await state.finish()