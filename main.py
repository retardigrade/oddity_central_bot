import os
import datetime
import asyncpg

import random
import requests
from bs4 import BeautifulSoup

import logging
from aiogram import Bot, Dispatcher, executor, types

ODDITY_BASE_URL = 'https://www.odditycentral.com/page/'
API_TOKEN = os.environ['API_TOKEN']
PG_PASSWORD = os.environ['POSTGRES_PASSWORD']

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    msg_text = "Send /weird to get a piece of weird news"
    await message.answer(msg_text)


@dp.message_handler(commands=['weird'])
async def send_news(message: types.Message):
    # gets random article from oddity and sends it to user
    page_number = random.randint(1, 642)
    page_url = ODDITY_BASE_URL + str(page_number)
    page_text = requests.get(page_url).text
    soup = BeautifulSoup(page_text, 'html.parser')
    articles = soup.find_all('a', {'rel': 'bookmark'})
    hrefs = [a['href'] for a in articles]
    chosen_href = random.choice(hrefs)
    await message.answer(chosen_href)

    # logs answer to database
    user_id = message.from_user.id
    user_name = message.from_user.username
    href = chosen_href
    time = str(datetime.datetime.now()).split('.')[0]
    record = "INSERT INTO public.sends VALUES ({},'{!s}','{!s}','{!s}')".format(user_id, user_name, time, href)
    conn = await asyncpg.connect('postgres://postgres:{pwd}@172.18.0.2:5432/postgres'.format(pwd=PG_PASSWORD))
    await conn.execute(record)
    await conn.close()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
