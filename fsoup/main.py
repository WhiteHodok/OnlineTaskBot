import asyncio
import datetime
import pytz
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
'''
Этот бот предназначен для отслеживания изменений в расписании группы АТП-221
Глубина поиска: 2 недели
Время обновления: 1 раз в 6 часов, с последующим уведомлением, если расписание изменилось
'''
def get_schedule():
    url = 'https://rasp.omgtu.ru/group/show/11138'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    schedule_table = soup.find('_ngcontent-c8', {'class': 'media day ng-star-inserted'})
    schedule = []
    schedule_table = soup.find('_ngcontent-c8', {'class': 'media day ng-star-inserted'})
    if schedule_table is None:
        raise ValueError("Unable to locate schedule table on webpage")
    for row in schedule_table.find_all('tr')[1:]:
        columns = row.find_all('td')
        schedule.append({
            'time': columns[0].text.strip(),
            'subject': columns[1].text.strip(),
            'type': columns[2].text.strip(),
            'teacher': columns[3].text.strip(),
            'room': columns[4].text.strip(),
        })
    return schedule


bot_token = ''
bot = Bot(token=bot_token)
dispatcher = Dispatcher(bot)

async def send_notification(chat_id, message):
    await bot.send_message(chat_id, message)

async def check_schedule():
    old_schedule = []
    while True:
        schedule = get_schedule()
        if schedule != old_schedule:
            message = 'Расписание на {} изменилось:\n\n'.format(datetime.date.today())
            for item in schedule:
                message += '{} {} {}\n{} {}\n\n'.format(item['time'], item['subject'], item['type'], item['teacher'], item['room'])
            await send_notification(chat_id, message)
            old_schedule = schedule
        await asyncio.sleep(60 * 60 * 24 * 7 * 2 - 60 * 60 * 6)

if __name__ == '__main__':
    chat_id = '415378656'
    loop = asyncio.get_event_loop()
    loop.create_task(check_schedule())
    executor.start_polling(dispatcher, loop=loop, skip_updates=True)
