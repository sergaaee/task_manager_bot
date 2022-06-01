from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher

token = "5244756589:AAEnSCCpTCQ18MjtCWfRGNT8PQuJdIDNKVs"
DB_PATH = "database/db"
storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
