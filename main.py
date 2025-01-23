import asyncio
from time import sleep

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from models import init, create_or_update_user, get_user, get_login
from request_login import login_main, login

# Load sensitive data from environment variables (use dotenv or similar library)
BOT_TOKEN = '7374450108:AAFP-xIaDYflJwsihKjbhvxgjuOhkmm8dA0'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Register(StatesGroup):
    name = State()
    class_grade = State()
    grade_number = State()
    grade_letter = State()


def grade_buttons():
    letters = ['A', 'B', 'V', 'G']
    inline_keyboard = []
    row = []

    for i in range(6, 12):
        for j in range(len(letters)):
            row.append(
                InlineKeyboardButton(text=f"{i} {letters[j]}", callback_data=f"grade.{i}_{letters[j]}")
            )
            if len(row) == 4:  # Add the row to the keyboard when it reaches 5 buttons
                inline_keyboard.append(row)
                row = []  # Reset the row

    if row:  # Add any remaining buttons to the keyboard
        inline_keyboard.append(row)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await message.answer(
        f"Hello {message.from_user.first_name}! Welcome to the bot {message.from_user.first_name}.\nBotga Login va parol  qoshish uchun shu usulda foydalaning\n\n👇👇👇👇👇👇👇👇👇👇👇👇👇add login(1):parol(1),login(2):parol(2)")


@dp.message(F.text.startswith("add"))
async def add(message: Message):
    try:
        if not ':' in message.text:
            await message.answer('Iltimos pasdagi korinishda  yozing\n add login:parol,login:parol')
            return
        data = message.text.split("add")[1].strip().split(",")
        ready = await login_main(data, tg_id=message.from_user.id)
        if len(ready[0]) != 0:
            text = f"❗️❗️❗️Wrong logins (Notogri loginlar login yoki parrol xato bolishi aniq xazilmas) ❗️❗️❗️\n"
            for i in ready[0]:
                text += i
                if ready[1] != 0:
                    await message.answer(text=f"Successful logins count✅: {ready[1]} \nSuccessful logins: {ready[3]}")
            await message.answer(text=f"{text}")
        await message.answer(text=f"successful logins number ✅ {ready[1]}")
        await message.answer(text='Sizga kunlik malumot kelsinmi?',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ha ✅',callback_data='t_yes'),InlineKeyboardButton(text='Yo`q ❌',callback_data='t_no')]]))

    except Exception as error:
        await message.answer(f"An error occurred: {str(error)}")
        print(f"Error in 'add' function: {error}")

@dp.callback_query(F.data.startswith("t"))
async def t_yes(callback_data:CallbackQuery):
    data = callback_data.data.split("t_")[1]
    if data == "yes":
        await create_or_update_user(name=callback_data.from_user.first_name,tg_id=str(callback_data.from_user.id),sending=True)
    else:
        await create_or_update_user(name=callback_data.from_user.first_name,tg_id=str(callback_data.from_user.id),sending=False)
    await callback_data.message.delete()
    await callback_data.answer(text='Siz xabar jonatishni tastiqladingiz ✅',show_alert=True)

async def test(data: int, tg_id):
    data = data
    await bot.send_message(text=f'{data}', chat_id=tg_id)

@dp.message(F.text=='data')
async def data(message: Message):
    data = await get_login()
    await message.answer(text=f"Jami {len(data)} dona login bor")
    for i in data:
        await message.answer(text=f"ID: {i.id}\nLogin: {i.login} parol: {i.password}\n🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵🪵")

@dp.message(F.text=='>:)')
async def start2(message: Message):
    log = await login()
    user_id = await get_user()
    for user in user_id:
        await bot.send_message(text=f"Kirish oxshamagan loginlar:  {log[0]}\nMuaffaqiyatli kirilgan loginlar soni:  {log[1]}",chat_id=user)
        await message.answer(text='Sizga kunlik malumot kelsinmi?',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ha ✅',callback_data='t_yes'),InlineKeyboardButton(text='Yo`q ❌',callback_data='t_no')]]))
    for i in range(0,730,1):
        print(i)
        sleep(60*60*12)
        log = await login()
        user_id = await get_user()
        for user in user_id:
            await bot.send_message(text=f"Kirish oxshamagan loginlar:  {log[0]}\nMuaffaqiyatli kirilgan loginlar soni:  {log[1]}",chat_id=user)
            await message.answer(text='Sizga kunlik malumot kelsinmi?',reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Ha ✅',callback_data='t_yes'),InlineKeyboardButton(text='Yo`q ❌',callback_data='t_no')]]))


async def main():
    await init()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye!")
