import os
import time
import datetime
import asyncio
import requests
from lxml import html
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog import Window

TOKEN = ''
if TOKEN is None:
    raise ValueError('Telegram token not found in environment variables')


CHAT_ID = ""
if CHAT_ID is None:
    raise ValueError('Chat ID not found in environment variables')



bot = Bot(token=TOKEN)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class ScheduleUpdate(StatesGroup):
    checking = State()
    found_change = State()

async def get_schedule():
    url = "https://rasp.omgtu.ru/group/show/11138"
    response = requests.get(url)
    page = html.fromstring(response.text)
    schedule_table = page.xpath('//table[@class="table table-bordered table-hover table-condensed"]/tbody')[0]
    return schedule_table.text_content()

async def check_schedule():
    async with ScheduleUpdate.checking:
        schedule = await get_schedule()
        if 'Changes not found' not in schedule:
            async with FSMContext.get_default().proxy() as data:
                last_update = data.get('last_update')
                if last_update is None or last_update != schedule:
                    data['last_update'] = schedule
                    await ScheduleUpdate.found_change.set()
        await asyncio.sleep(60 * 60 * 6)  # check again in 6 hours
        await check_schedule()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Я помогу тебе не перепутать пары.")
    await check_schedule()

@dp.message_handler(state=ScheduleUpdate.found_change)
async def found_change(message: types.Message, state: FSMContext):
    await message.answer("Расписание поменялось! Вот детали:\n")
    async with state.proxy() as data:
        last_update = data.get('last_update')
        if last_update is not None:
            await message.answer(last_update)
        else:
            await message.answer("Я не могу найти изменения.")
    await state.finish()

if __name__ == '__main__':
    asyncio.run(dp.start_polling())
