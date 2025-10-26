import requests
import asyncio
from bs4 import BeautifulSoup
from telebot import types
import telebot
from telebot.async_telebot import AsyncTeleBot

bot= AsyncTeleBot('YOUR TOKEN HERE')

@bot.message_handler(commands=['start'])
async def start(message):
    kb= types.ReplyKeyboardMarkup(
        row_width=1, resize_keyboard=True, one_time_keyboard=True
    )
    btn= types.KeyboardButton(text='<UNK> <UNK>', request_location=True)
    kb.add(btn)
    await bot.send_message(message.chat.id, 'Нажми кнопку для отправления местоположения', reply_markup=kb)


@bot.message_handler(content_types=['location'])
async def location(message):
    lat = message.location.latitude
    lon = message.location.longitude
    url1 = f'https://yandex.ru/pogoda/ru?lat={lat}&lon={lon}'
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, 'lxml')
    znach= soup.find('span', class_= "AppFactTemperature_sign__1MeN4")
    temperature= soup.find('span', class_= "AppFactTemperature_value__2qhsG")
    #cell= soup.find('span', class_= "AppFactTemperature_degree__LL_2v")

    await bot.reply_to(message, f'Температура в вашем регионе {znach.text} {temperature.text}')

if __name__ == "__main__":
    asyncio.run(bot.polling())
