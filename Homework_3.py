from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command

router = Router()

# --- Reply клавиатура для выбора языка ---
keyboard_lang = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Python")],
        [KeyboardButton(text="JavaScript")],
        [KeyboardButton(text="C#")]
    ],
    resize_keyboard=True
)

# --- Inline клавиатура для /help ---
inline_help = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Документация Python", url="https://docs.python.org/3/"),
        ],
        [
            InlineKeyboardButton(text="Документация JS", url="https://developer.mozilla.org/en-US/docs/Web/JavaScript"),
        ],
        [
            InlineKeyboardButton(text="Документация C#", url="https://learn.microsoft.com/en-us/dotnet/csharp/"),
        ],
        [
            InlineKeyboardButton(text="Начать обучение", callback_data="start_learning"),
        ]
    ]
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f'Привет {message.from_user.first_name}! Я твой первый бот.\n'
        f'Выбери язык программирования:',
        reply_markup=keyboard_lang
    )
    print(f"Пользователь {message.from_user.full_name} отправил {message.text} в {message.date}")


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(
        '/start - приветствие и выбор языка\n'
        '/help - список команд + ссылки\n'
        '/about - информация о боте',
        reply_markup=inline_help
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


@router.callback_query(F.data == "start_learning")
async def start_learning(callback: CallbackQuery):
    await callback.answer("Начинаем обучение!", show_alert=True)


# --- Обработка выбора языка ---
@router.message(F.text == "Python")
async def info_python(message: Message):
    await message.answer("Python — универсальный язык, прост в изучении, отлично подходит для бэкенда, анализа данных и автоматизации.")

@router.message(F.text == "JavaScript")
async def info_js(message: Message):
    await message.answer("JavaScript — главный язык веба, работает в браузере и на сервере (Node.js).")

@router.message(F.text == "C#")
async def info_csharp(message: Message):
    await message.answer("C# — язык от Microsoft, используется для разработки приложений, игр (Unity) и корпоративных систем.")


@router.message(F.text == "Корзина")
async def get_group(message: Message):
    await message.answer("привет, примерно вот твоя корзина !!!!")


@router.message()
async def echo(message: Message):
    await message.answer(f"Ты написал: {message.text}")
