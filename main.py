from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN , CON
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time


cur = CON.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    count INTEGER
    )""")
CON.commit()

async def db_table_value(name:str, price:int, count:int):
    cur.execute(f"INSERT INTO products (name, price, count) VALUES ('{name}', {price}, {count})")
    CON.commit()
    return


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply('Привет! Напиши /help для получения списка команд.')


@dp.message_handler(commands=['help'])
async def help(message):
    await message.reply('Доступные команды: /push\nПосле введения команды /push я начну закидывать вещи которые ты купил в базу данных.')
    return 


class Info_product:
    def __init__(self,name:str):
        self.name = name
        self.price = None
        self.count = None    
    def __push__(self):
        cur.execute(f"INSERT INTO products (name, price, count) VALUES ('{self.name}', {self.price}, {self.count})")
        CON.commit()
        return cur.execute(f"SELECT * FROM products WHERE name = '{self.name}'").fetchall()

@dp.message_handler(commands=['push'])
async def push_to_db(msg: types.Message):
    product_name = msg.text
    product_name = product_name.split()
    await db_table_value(product_name[1], int(product_name[2]), int(product_name[3]))



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)