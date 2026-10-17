import asyncio
from datetime import datetime
import pytz
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# === НАСТРОЙКИ ===
BOT_TOKEN = "8947446124:AAFzzu2a1zBOHFGnfR7wPNxbpwVUk71K3vY"  # Твой токен от BotFather

# Дата рождения подруги (Год, Месяц, День)
BIRTHDAY = datetime(2026, 10, 20).date()

TIMEZONE = pytz.timezone("Europe/Moscow")

# Время отправки — ровно в полночь (00:00)
SEND_HOUR = 0
SEND_MINUTE = 0

user_chat_id = None
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler(timezone=TIMEZONE)


# Обработка команды /start
@dp.message(CommandStart())
async def start_handler(message: Message):
    global user_chat_id
    user_chat_id = message.chat.id
    await message.answer("Привет! Совсем скоро твой праздник! ✨")


# Функция ежедневной проверки и отправки
async def send_daily_reminder():
    global user_chat_id
    if user_chat_id is None:
        return

    today = datetime.now(TIMEZONE).date()
    days_left = (BIRTHDAY - today).days

    # Отправляем сообщения только если осталось 2, 1 или 0 дней
    if days_left == 2:
        await bot.send_message(chat_id=user_chat_id, text="Привет, Полиночкаааааааааааааааааааа! До твоего дня рождения осталось всего 2 дня!✨")
    elif days_left == 1:
        await bot.send_message(chat_id=user_chat_id, text="До твоего дня рождения остался 1 день! Готовься принимать комплименты, подарки и вспеобщее обаяние🎉")
    elif days_left == 0:
        # В день рождения в 00:00 отправляем поздравление и твоё видео!
        text = "Моя дорогая, с днём рождения! ❤️ Нашей дружбе уже целых 5 лет, и за это время ты стала для меня не просто лучшей подругой, а по-настоящему родным человеком. Спасибо тебе за каждую нашу встречу, за разговоры обо всём на свете, за поддержку и за то, что с тобой всегда можно посмеяться от души. Я безумно благодарна судьбе за то, что ты есть в моей жизни. Желаю тебе невероятного счастья, пусть всё задуманное сбывается легко и именно так, как ты мечтаешь. Сияй, улыбайся и помни, какая ты потрясающая! Я всегда рядом, что бы ни случилось. Очень тебя люблю! С твоим днём! 🎉🎂✨"

        # Твой file_id видео, который мы получили ранее:
        VIDEO_ID = "BAACAgIAAxkBAAMDatOAcFlZ2l7KPTiutPo43hSX31AAAtWuAAL24qBKCNDJLpjmX-w9BA"

        try:
            await bot.send_video(
                chat_id=user_chat_id,
                video=VIDEO_ID,
                caption=text
            )
        except Exception:
            await bot.send_message(chat_id=user_chat_id, text=text)


async def main():
    scheduler.add_job(
        send_daily_reminder,
        trigger="cron",
        hour=SEND_HOUR,
        minute=SEND_MINUTE
    )
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
