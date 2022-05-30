from aiogram.contrib.fsm_storage.memory import MemoryStorage
from settings import token
from aiogram import Bot, Dispatcher, executor


# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)


def main():
    from async_tasks.notifications import start_check
    import message_handlers
    # Configure logging
    message_handlers.logging.basicConfig(level=message_handlers.logging.INFO)
    # bot start
    executor.start_polling(message_handlers.dp, skip_updates=True, on_startup=start_check)


if __name__ == '__main__':
    main()
