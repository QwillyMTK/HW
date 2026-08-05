import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, Router, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# --- сюда вставляешь токен ---
API_TOKEN = "ТОКЕН_ТВОЕГО_БОТА"

router = Router()

# --- Работа с БД ---
DB_NAME = "questions.db"

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    answer TEXT NOT NULL
);
"""

CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE,
    username TEXT,
    score INTEGER DEFAULT 0
);
"""

INSERT = "INSERT INTO questions (text, answer) VALUES (?, ?);"
SELECT_ALL = "SELECT id, text, answer FROM questions;"
DELETE = "DELETE FROM questions WHERE id = ?;"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    cursor.execute(CREATE_USERS)
    conn.commit()
    conn.close()

def add_question(text: str, answer: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(INSERT, (text, answer))
    conn.commit()
    conn.close()

def get_all_questions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SELECT_ALL)
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_question(q_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(DELETE, (q_id,))
    conn.commit()
    conn.close()

# --- Работа с пользователями ---
def update_user_score(user_id: int, username: str, score: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (user_id, username, score) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id) DO UPDATE SET score = score + ?;",
        (user_id, username, score, score)
    )
    conn.commit()
    conn.close()

def get_top_users(limit: int = 3):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT username, score FROM users ORDER BY score DESC LIMIT ?;", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Состояния викторины ---
class QuizStates(StatesGroup):
    question = State()
    result = State()

# --- Вопросы викторины (статичные) ---
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

# --- Команды ---
@router.message(CommandStart())
async def cmd_start(message: Message):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать викторину 🎮", callback_data="quiz_start")]
        ]
    )
    await message.answer("Привет! Давай проверим твои знания SQL и БД.", reply_markup=kb)

@router.message(Command("list"))
async def list_questions(message: Message):
    questions = get_all_questions()
    if not questions:
        await message.answer("В базе пока нет вопросов.")
        return
    text = []
    for q in questions:
        text.append(f"{q[0]}. {q[1]} — [{q[2]}]")
    await message.answer("\n".join(text))

@router.message(Command("add"))
async def add_q(message: Message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        await message.answer("Используй: /add [текст] [ответ]")
        return
    text, answer = args[1], args[2]
    add_question(text, answer)
    await message.answer(f"Вопрос добавлен: {text} — [{answer}]")

@router.message(Command("del"))
async def del_q(message: Message):
    args = message.text.split()
    if len(args) != 2 or not args[1].isdigit():
        await message.answer("Используй: /del [ID]")
        return
    q_id = int(args[1])
    delete_question(q_id)
    await message.answer(f"Вопрос с ID {q_id} удалён.")

# --- Команда /rating ---
@router.message(Command("rating"))
async def rating(message: Message):
    users = get_top_users()
    if not users:
        await message.answer("Пока нет данных о пользователях.")
        return
    text = ["🏆 Топ-3 игроков:"]
    for i, (username, score) in enumerate(users, start=1):
        text.append(f"{i}. {username or 'Без имени'} — {score} очков")
    await message.answer("\n".join(text))

# --- Викторина ---
@router.callback_query(F.data == "quiz_start")
async def quiz_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(score=0, index=0)
    await callback.answer("Начинаем викторину!", show_alert=True)
    await send_question(callback.message, state)

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
        # сохраняем результат
        update_user_score(message.from_user.id, message.from_user.username, score)

        await message.answer(
            f"Тест окончен! Ваш результат: {score}/{len(quiz_questions)}",
            reply_markup=play_again_keyboard()
        )
        await state.clear()

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
    init_db()  # создаём таблицы, если их нет
    bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
