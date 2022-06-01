import logging
from aiogram import executor
from async_tasks import start_check
from settings import dp


if __name__ == '__main__':
    import handlers
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=start_check)
