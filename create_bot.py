from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from config import TOKEN
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from data_base.sqlite_db import DataBase

storage = MemoryStorage()
data_base = DataBase('history.db')
my_bot = Bot(token=TOKEN)
dp = Dispatcher(my_bot, storage=storage)