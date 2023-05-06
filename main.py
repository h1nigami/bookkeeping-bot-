from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN , CON
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import time


CUR = CON.cursor()
CUR.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    count INTEGER
    )""")
CON.commit()

async def db_table_value(name:str, price:int, count:int):
    CUR.execute(f"INSERT INTO products (name, price, count) VALUES ('{name}', {price}, {count})")
    CON.commit()
    return


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    button = KeyboardButton('/help')
    KeyboardButtons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button)
    await message.reply('Привет! Напиши /help для получения списка команд.', reply_markup=KeyboardButtons)


@dp.message_handler(commands=['help'])
async def help(message):
    buttons = [(KeyboardButton('/push')), (KeyboardButton('/off')), (KeyboardButton('/show'))]
    KeyboardButtons = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*buttons)
    await message.reply('''Доступные команды: /push, /off, /show.\n
После введения команды /push введи вещи которые ты купил, я закину в базу данных\n
После введения команды /off я выключу бота.\n
После введения команды /show я вывожу все вещи из базы данных в виде упорядоченного списка.\n''', reply_markup=KeyboardButtons)    
    return 


class Info_product:
    def __init__(self,name:str):
        self.name = name
        self.price = None
        self.count = None    
    def __push__(self):
        CUR.execute(f"INSERT INTO products (name, price, count) VALUES ('{self.name}', {self.price}, {self.count})")
        CON.commit()
        return CUR.execute(f"SELECT * FROM products WHERE name = '{self.name}'").fetchall()

@dp.message_handler(commands=['push'])
async def push_to_db(msg: types.Message):
    product_name = msg.text
    product_name = product_name.split()
    await db_table_value(product_name[1], int(product_name[2]), int(product_name[3]))
    await msg.reply('Хороший выбор')


@dp.message_handler(commands=['off'])
async def power_off(message):
    try:
        import os
        await message.reply('Выключаюсь')
        os.system('shutdown /s /t 1')
    except:
        await message.reply('Что то мешает мне выключится')
    return

@dp.message_handler(commands=['show'])
async def show_db(message):
    await message.reply(CUR.execute(f"SELECT * FROM products").fetchall())
    return

if __name__ == '__main__':
    executor.start_polling(dp)
