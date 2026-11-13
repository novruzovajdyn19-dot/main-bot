from os import getenv
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import ( 
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.enums import ChatMemberStatus
from dotenv import load_dotenv

load_dotenv()

router = Router()

ADMIN_ID = int(getenv("ADMIN_ID", 0))
CHANNEL_ID = int(getenv("CHANNEL_ID", 0))
FILE_PATH = "saved_messages.txt"

@router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        '👋 Добро пожаловать в анонимный чат!\n'
        'Здесь ты можешь поделиться своими мыслями, историями, признаниями или просто написать то, что давно хотел сказать.\n\n'
        '🔒 Как это работает?\n'
        '1. Напиши сообщение этому боту.\n'
        '2. Отправь его.\n'
        '3. После проверки сообщение будет опубликовано в нашем Telegram-канале.\n'
        '4. Твоя личность не будет указана при публикации.\n\n'
        '📄 Продолжая использование бота, ты соглашаешься с Пользовательским соглашением.\n\n'
        'Готов поделиться чем-то? Просто отправь сообщение ниже!'
    )

@router.message()
async def check_subscription(message: Message):
    """Проверка подписки пользователя на канал"""
    user_id = message.from_user.id
    
    if user_id == ADMIN_ID:
        return

    try:
        member = await message.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR
        ]:
            return 
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/thechatarchive")]
            ])
            await message.answer("Чтобы пользоваться ботом, пожалуйста, подпишитесь на наш канал:", reply_markup=keyboard)
            return
    except Exception as e:
        print(f"Ошибка при проверке подписки: {e}")

@router.message(F.text)
async def save_user_message(message: Message):
    """Сохранение и отправка сообщения в канал"""
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    text = message.text
    log_entry = (
        f"Имя: {full_name}\n"
        f"ID: {user_id}\n"
        f"Сообщение: {text}\n"
        f"--------------------------------------------------\n\n"
    )
    with open(FILE_PATH, "a", encoding="utf-8") as file:
        file.write(log_entry)

    if user_id == ADMIN_ID:
        log_ch_entry = f"{text} - admin"
    else:
        log_ch_entry = f"{text} - user"

    try:
        await message.bot.send_message(
            chat_id=CHANNEL_ID, 
            text=log_ch_entry
        )
    except Exception as e:
        print(f"Ошибка при отправке в канал: {e}")
        
    await message.answer("Ваше сообщение получено и передано!")