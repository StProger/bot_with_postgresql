from data_user import API, user_psql, pw_psql
import logging
import psycopg2
import requests
from aiogram import Bot, Dispatcher, executor, types
import datetime
API_TOKEN = '6281292271:AAHgw6JJKHhY-7YkXVRnxeiE8pcK04miQaA'
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

conn = psycopg2.connect(database = 'weather_bot',
                        user = user_psql,
                        password = pw_psql,
                        host = 'localhost',
                        port = '5432')
cursor = conn.cursor()

url = 'https://api.openweathermap.org/data/2.5/weather'


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Hello, I am weather bot. I will tell you about weather. Write city.")

@dp.message_handler()
async def weather(message):
    params = {
        'q':message.text,
        'units':'metric',
        'lang':'ru',
        'APPID':API
    }
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    time = datetime.datetime.now().strftime('%H:%M:%S')
    try:
        res = requests.get(url, params=params).json()
        city = res['name']
        discription = res['weather'][0]['description'].capitalize()
        temp = res['main']['temp']
        wind_speed = res['main']['temp']
        await message.answer(f"{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n"
                             f"Погода в {city}:\n"
                             f"{discription.capitalize()}\n"
                             f"Температура: {temp}C°\n"
                             f"Скорость ветра: {wind_speed}м/с")
        query = "INSERT INTO data (weather, temp, wind_speed, time, date) VALUES(%s, %s, %s, %s, %s)"
        data = (discription, temp, wind_speed, time, date)
        cursor.execute(query, data)
        conn.commit()
    except:
        await message.answer('Кажется, вы ввели неправильно название города.')

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)