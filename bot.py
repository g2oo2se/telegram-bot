import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# ============================================================
# НАСТРОЙКИ (БЕРУТСЯ ИЗ ПЕРЕМЕННЫХ ОКРУЖЕНИЯ НА RENDER)
# ============================================================

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_ID = 982987647
PRICE = 1500
CARD_NUMBER = "5536 9100 1817 2900"

# Проверка: если токен не задан — бот не запустится
if not BOT_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не задан! Добавь переменную окружения на Render.")

# ============================================================
# КОД БОТА (НЕ ТРОГАЙ)
# ============================================================

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главная клавиатура
def main_menu():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛒 Купить карточку", callback_data="buy")],
        [InlineKeyboardButton(text="🎵 Посмотреть демо", callback_data="demo")],
        [InlineKeyboardButton(text="📖 Инструкция", callback_data="info")]
    ])
    return keyboard

# Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    text = (
        "🎵 *Добро пожаловать в BLACK CARD SHOP!*\n\n"
        "Этот бот продаёт интерактивную карточку для артиста с виниловым плеером.\n\n"
        "📌 *Что внутри:*\n"
        "✅ Эффект открытия\n"
        "✅ 3D-переворот\n"
        "✅ Виниловый плеер с перемоткой\n"
        "✅ Полный адаптив под телефон\n\n"
        "💰 *Цена: 1500 ₽*\n\n"
        "Выбери действие ниже 👇"
    )
    await message.answer(text, reply_markup=main_menu(), parse_mode="Markdown")

# Обработка кнопок
@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    if callback.data == "buy":
        text = (
            "💳 *Оплата*\n\n"
            "Переведи *1500 ₽* на карту:\n"
            f"`{CARD_NUMBER}`\n\n"
            "После оплаты нажми кнопку ниже, я проверю и вышлю карточку.\n\n"
            "📌 *Важно:* в комментарии укажи свой Telegram-ник"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Я оплатил", callback_data="paid")]
        ])
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
        await callback.answer()

    elif callback.data == "paid":
        text = (
            "✅ *Отлично!*\n\n"
            "Я проверю оплату и отправлю тебе карточку в ближайшее время.\n\n"
            "Если всё ок — файл придёт сюда в течение 5–10 минут.\n"
            "Если возникнут вопросы — пиши @zoo2se"
        )
        await bot.send_message(
            ADMIN_ID,
            f"🔔 Новый покупатель!\n"
            f"Пользователь: @{callback.from_user.username or callback.from_user.first_name}\n"
            f"ID: {callback.from_user.id}"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")
        await callback.answer()

    elif callback.data == "demo":
        text = (
            "🎬 *Демо-версия*\n\n"
            "Вот как выглядит карточка:\n\n"
            "👉 [Ссылка на видео-демо](https://youtu.be/...)\n"
            "или\n"
            "👉 [Ссылка на рабочий пример](https://твой-сайт.github.io)\n\n"
            "Посмотри и возвращайся к покупке 😉"
        )
        await callback.message.edit_text(text, parse_mode="Markdown")
        await callback.answer()

    elif callback.data == "info":
        text = (
            "📖 *Инструкция*\n\n"
            "1️⃣ Открой файл `index.html` в текстовом редакторе\n"
            "2️⃣ Найди места с пометкой `[ЗАМЕНИТЕ]`\n"
            "3️⃣ Вставь своё фото, трек, имя, жанр\n"
            "4️⃣ Сохрани и открой в браузере\n\n"
            "Всё просто! Готово за 5 минут."
        )
        await callback.message.edit_text(text, parse_mode="Markdown")
        await callback.answer()

# Запуск бота
async def main():
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
