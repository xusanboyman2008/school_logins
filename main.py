import asyncio

from aiogram.exceptions import TelegramBadRequest

from models import init
import pytz
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keep_alive import keep_alive
from models import get_users, create_user, get_login1, get_users_all
from request_login import login_main, login

# Load sensitive data from environment variables (use dotenv or similar library)
# BOT_TOKEN = "7894961736:AAGwAqAzmoMdUYye1-CuU9sf5Db-iKeVdmQ"
BOT_TOKEN = "7374450108:AAFEg4iriMNqGiHk09Z3TJ_JCYuLZMOleLE"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
UZBEKISTAN_TZ = pytz.timezone("Asia/Tashkent")


class Register(StatesGroup):
    name = State()
    class_grade = State()
    grade_number = State()
    grade_letter = State()

class Send(StatesGroup):
    starr = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    commands = [
        BotCommand(command="/start", description="Botni boshlash"),
        BotCommand(command="/help", description="Yordam olish")
    ]
    await bot.set_my_commands(commands=commands)
    await create_user(name=f"{message.from_user.first_name}", tg_id=message.from_user.id,
                      sending=False)
    await message.answer(
        f"Hello ! Welcome to the bot {message.from_user.first_name}.\nBotga Login va parol  qoshish uchun shu usulda foydalaning\n\n👇👇👇👇👇👇👇👇👇👇👇👇👇\nadd login(1):parol(1),login(2):parol(2)")


@dp.message(F.text.startswith("add"))
async def add(message: Message):
    try:
        if not ":" in message.text:
            await message.answer("Iltimos pasdagi korinishda  yozing\n add login1:parol1,login2:parol2")
            return
        data = message.text.split("add")[1].strip().split(",")
        await message.answer(text=f'Jami {len(data)} login uchun taxminan {len(data)*3} sekund 🕔 vaqt ketadi')
        ready = await login_main(data)
        if len(ready[0]) != 0:
            text = f"❗️❗️❗️️Wrong logins or password❗️❗️❗️️\n"
            for i in ready[0]:
                text += i
                if ready[1] != 0:
                    await message.answer(text=f"Successful logins count✅: {ready[1]} \nSuccessful logins: {ready[3]}")
            await message.answer(text=f"{text}")
        await message.answer(text=f"successful logins number ✅ {ready[1]}")
        await message.answer(text="Sizga kunlik malumot kelsinmi?", reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Ha ✅", callback_data="t_yes"),
             InlineKeyboardButton(text="Yo`q ❌", callback_data="t_no")]]))

    except Exception as error:
        await message.answer(f"An error occurred: {str(error)}")
        print(f"Error in 'add' function: {error}")


@dp.callback_query(F.data.startswith("t"))
async def t_yes(callback_data: CallbackQuery):
    data = callback_data.data.split("t_")[1]
    if data == "yes":
        await create_user(name=f"{callback_data.from_user.first_name}", tg_id=callback_data.from_user.id,
                                    sending=True)
    else:
        await create_user(name=callback_data.from_user.first_name, tg_id=callback_data.from_user.id,
                                    sending=False)
    await callback_data.message.delete()
    await callback_data.answer(text="Siz xabar jonatishni tastiqladingiz ✅", show_alert=True)


async def test(data: int, tg_id):
    data = data
    await bot.send_message(text=f"{data}", chat_id=tg_id)


@dp.message(F.text == "data")
async def data(message: Message):
    data = await get_login1()
    await message.answer(text=f"Jami {len(data)} dona login bor")
    text = ''
    for i in data:
            text+=f"ID: {i.id}\nLogin: {i.login} parol: {i.password} status: {i.status}\n🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵\n"
    await message.answer(text=text)

@dp.message(F.text == "/help")
async def help(message: Message):
    await message.answer(text='Agarda sizning savollaringiz bolsa 👇 Bot yaratuvchisiga yozing\n<a href="https://t.me/xusanboyman200/">Admin</a>',parse_mode="HTML")

scheduler = AsyncIOScheduler()



# Function to send daily updates at 8:00 AM
async def send_daily_update():
        log = await login()
        user_ids = await get_users()
        for user_id in user_ids:
            try:
                if user_id.role == 'Admin':
                    await bot.send_message(
                    text=f"Kirish oxshamagan loginlar soni ❌: {len(log[0].split(','))}\nMuaffaqiyatli kirilgan loginlar soni ✅: {log[1]}\nKirilmagan loginlar\n\n{log[0]}",
                    chat_id=user_id.tg_id
                )
                else:
                    await bot.send_message(
                        text=f"Kirish oxshamagan loginlar soni ❌: {len(log[0])}\nMuaffaqiyatli kirilgan loginlar soni ✅: {log[1]}\n",
                        chat_id=user_id.tg_id
                    )
            except TelegramBadRequest as e:
                continue

@dp.message(F.text=='login')
async def logins_all(message:Message):
    await message.answer(text='Sending...')
    await send_daily_update()

@dp.message(F.text == 'send')
async def send_all_users(message: Message, state: FSMContext):
    await message.answer('nima jonatsangiz ham jonating')
    await state.set_state(Send.starr)

@dp.message(Send.starr)
async def starr(message: Message, state: FSMContext):
    users = await get_users_all()  # Get the list of users
    if not users:
        await message.answer("No users found.")
        await state.clear()
        return

    for user_id in users:
        if message.text:
            await bot.send_message(text=message.text, chat_id=user_id)
        elif message.photo:
            await bot.send_photo(caption=message.text, chat_id=user_id, photo=message.photo[-1].file_id)
        elif message.sticker:
            for i in range(740,810):
                print(i,user_id)
                await bot.send_sticker(chat_id=user_id, sticker=message.sticker.file_id)
        elif message.video:
            await bot.send_video(video=message.video[-1].file_id, chat_id=user_id)
        elif message.audio:
            await bot.send_audio(audio=message.audio[-1].file_id, chat_id=user_id)

    await state.clear()  # Clear the state after sending the messages to all users
    await message.answer("Message sent to all users.")




async def main2():
    scheduler.add_job(
        send_daily_update,
        trigger="cron",
        hour=8,
        minute=0,
        timezone=UZBEKISTAN_TZ,
    )
    await init()
    scheduler.start()
    keep_alive()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main2())

