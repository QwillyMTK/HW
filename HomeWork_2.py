from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from src.keyboards import keyboard_main, inline


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.first_name}! Я твой первый бот.',
        reply_markup=keyboard_main
    )
    print(f"Пользователь {message.from_user.full_name} отправил {message.text} в {message.date}")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - приветствие\n'
        '/help - список команд\n'
        '/about - информация о боте',
        reply_markup=inline
    )


@router.message(Command('about'))
async def cmd_about(message: Message):
    await message.answer(
        "Я бот Qwilly, создан 1.07.2026.\n"
        "Могу помочь тебе с поиском информации,\n"
        "или можем поиграть в угадайку 🎮"
    )


@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery):
    await callback.answer('Вы готовы?', show_alert=True)
    await callback.message.answer("Начинаем тест!")


@router.message(F.text == "Корзина")
async def get_group(message: Message):
    await message.answer("привет, примерно вот твоя корзина !!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")
