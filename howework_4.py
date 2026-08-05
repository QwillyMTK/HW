import asyncio
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


API_TOKEN = "токен"

router = Router()

# --- Состояния викторины ---
class QuizStates(StatesGroup):
    question = State()
    result = State()

# --- Вопросы викторины ---
quiz_questions = [
    {"q": "Что означает SQL?", "options": ["Structured Query Language", "Simple Query Logic", "System Quality Level"], "answer": "Structured Query Language"},
    {"q": "Какая команда используется для выборки данных?", "options": ["SELECT", "INSERT", "UPDATE"], "answer": "SELECT"},
    {"q": "Какая команда добавляет новую строку?", "options": ["INSERT", "DELETE", "ALTER"], "answer": "INSERT"},
    {"q": "Какая команда изменяет существующие данные?", "options": ["UPDATE", "DROP", "CREATE"], "answer": "UPDATE"},
    {"q": "Какая команда удаляет таблицу?", "options": ["DROP", "DELETE", "REMOVE"], "answer": "DROP"},
]

# --- Кнопка для повторной игры ---
def play_again_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Сыграть снова 🎮", callback_data="quiz_start")]
        ]
    )

# --- Запуск викторины ---
@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать викторину 🎮", callback_data="quiz_start")]
        ]
    )
    await message.answer("Привет! Давай проверим твои знания SQL и БД.", reply_markup=kb)

@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(score=0, index=0)
    await callback.answer("Начинаем викторину!", show_alert=True)
    await send_question(callback.message, state)

# --- Отправка вопроса ---
async def send_question(message: Message, state: FSMContext):
    data = await state.get_data()
    index = data["index"]

    if index < len(quiz_questions):
        q = quiz_questions[index]
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=opt, callback_data=f"answer:{opt}")]
                for opt in q["options"]
            ]
        )
        await message.answer(f"Вопрос {index+1}: {q['q']}", reply_markup=keyboard)
        await state.set_state(QuizStates.question)
    else:
        score = data["score"]
        await message.answer(
            f"Тест окончен! Ваш результат: {score}/{len(quiz_questions)}",
            reply_markup=play_again_keyboard()
        )
        await state.clear()

# --- Обработка ответа ---
@router.callback_query(F.data.startswith("answer:"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    index = data["index"]
    q = quiz_questions[index]
    answer = callback.data.split(":", 1)[1]

    if answer == q["answer"]:
        await state.update_data(score=data["score"] + 1)
        await callback.answer("Верно ✅", show_alert=True)
    else:
        await callback.answer("Неверно ❌", show_alert=True)

    await state.update_data(index=index + 1)
    await send_question(callback.message, state)

# --- Запуск бота ---
async def main():
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
