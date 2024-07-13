import logging
import os

from dotenv import load_dotenv
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor

logging.basicConfig(level=logging.INFO)
load_dotenv(".env")

API_TOKEN = os.getenv('TOKEN')

admin_id: int = int(os.getenv('ADMIN_ID'))

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    name = State()  # Familya Ism Sharif
    b_day = State()  # Tug'ilgan kun oy yil
    school = State()  # Maktabingiz va nechanchi sinfsiz
    location = State()  # Yashash manzil Tuman, Mahalla ko'cha uy
    hobby = State()  # Sevimli mashg'ulotlar
    job = State()  # Kelajakda kim bo'lmoqchisiz
    problem_s = State()  # Maktabdagi muammolar
    problem_f = State()  # Oiladagi muammolar
    offer = State()  # Taklifa va istaklar
    events = State()  # Qatnashgan tadbir tanlovlaringiz


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await Form.name.set()
    await bot.send_message(admin_id, f"id: {message.from_user.id}\nname: {message.from_user.full_name}")
    await message.reply(f"Assalomu alaykum botga xush kelibsiz.\n"
                        f"To'liq ismingizni kiriting (FIO)?")


@dp.message_handler(state=Form.name)
async def process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await Form.next()
    await message.reply("Tug'ilgan kuningiz (kun.oy.yil)?")


@dp.message_handler(state=Form.b_day)
async def process_b_day(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['b_day'] = message.text

    await Form.next()
    await message.reply("Ta'lim muassasangiz va sinfiningiz?")


@dp.message_handler(state=Form.school)
async def process_school(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['school'] = message.text

    await Form.next()
    await message.reply("Yashash manzilingiz\nTuman, Mahalla, Ko'cha Uy(bo'lsa)?")


@dp.message_handler(state=Form.location)
async def process_location(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['location'] = message.text

    await Form.next()
    await message.reply("Sevimli mashg'ulotingiz?")


@dp.message_handler(state=Form.hobby)
async def process_hobby(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hobby'] = message.text

    await Form.next()
    await message.reply("Kelajakda kim bo'lmoqchisiz?")


@dp.message_handler(state=Form.job)
async def process_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job'] = message.text

    await Form.next()
    await message.reply("Ta'lim muassasangiz bilan bog'liq qanday muammolar bor?")


@dp.message_handler(state=Form.problem_s)
async def process_problem_s(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problem_s'] = message.text

    await Form.next()
    await message.reply("Oilada qanday muammo sizni qiynayapti?")


@dp.message_handler(state=Form.problem_f)
async def process_problem_f(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['problem_f'] = message.text

    await Form.next()
    await message.reply("Taklif va istaklaringiz?")


@dp.message_handler(state=Form.offer)
async def process_offer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['offer'] = message.text

    await Form.next()
    await message.reply("Qaysi yo'nalishdagi tadbir va tanlovlarda ishtirok etishni hohlaysiz?")


@dp.message_handler(state=Form.events)
async def process_events(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data['events'] = message.text
    await bot.send_message(
        admin_id,
        md.text(
            md.text(md.bold(f"ID: {user_id} name: {message.from_user.full_name}\n")),
            md.text(md.bold("✅ Ro'yhatdan muvafaqiyatli o'tdingiz. \n")),
            md.text(md.bold("Sizning ma'lumotlaringiz:\n")),
            md.text(f"To'liq ismingiz: <b>{data['name']}</b>"),
            md.text(f"Tug'ilgan sanangiz: <b>{data['b_day']}</b>"),
            md.text(f"Ta'lim muassasangiz va sinfingiz: <b>{data['school']}</b>"),
            md.text(f"Yashash manzilingiz: <b>{data['location']}</b>"),
            md.text(f"Sevimli mashg'ulotingiz: <b>{data['hobby']}</b>"),
            md.text(f"Ta'lim muassasasiga bog'liq muammolaringiz: <b>{data['problem_s']}</b>"),
            md.text(f"Oiladagi muammolaringiz: <b>{data['problem_f']}</b>"),
            md.text(f"Sizning taklif va istaglaringiz: <b>{data['offer']}</b>"),
            md.text(f"Ishtirok etishni istaydigan tadbir va tanlovlar: <b>{data['events']}</b>"),
            sep='\n',
        ),
    )
    await bot.send_message(
        user_id,
        md.text(
            md.text("<b>✅ Ro'yhatdan muvafaqiyatli o'tdingiz.</b> \n"),
            md.text("<b>Sizning ma'lumotlaringiz:</b> \n"),
            md.text(f"To'liq ismingiz: <b>{data['name']}</b>"),
            md.text(f"Tug'ilgan sanangiz: <b>{data['b_day']}</b>"),
            md.text(f"Ta'lim muassasangiz va sinfingiz: <b>{data['school']}</b>"),
            md.text(f"Yashash manzilingiz: <b>{data['location']}</b>"),
            md.text(f"Sevimli mashg'ulotingiz: <b>{data['hobby']}</b>"),
            md.text(f"Ta'lim muassasasiga bog'liq muammolaringiz: <b>{data['problem_s']}</b>"),
            md.text(f"Oiladagi muammolaringiz: <b>{data['problem_f']}</b>"),
            md.text(f"Sizning taklif va istaglaringiz: <b>{data['offer']}</b>"),
            md.text(f"Ishtirok etishni istaydigan tadbir va tanlovlar: <b>{data['events']}</b>"),
            sep='\n',
        ),

        parse_mode=ParseMode.HTML,
    )
    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
