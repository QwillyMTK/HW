import sqlite3

# Создаём подключение и курсор
conn = sqlite3.connect(":memory:")  # база в памяти
cur = conn.cursor()

# --- Создание таблиц ---
cur.execute("""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    genre TEXT
)
""")

cur.execute("""
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    movie_id INTEGER,
    rating INTEGER CHECK(rating BETWEEN 1 AND 10),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
)
""")

# --- Данные ---
cur.executemany("INSERT INTO users (name) VALUES (?)", [
    ("Алексей",), ("Мария",), ("Иван",), ("Ольга",), ("Даниил",)
])

cur.executemany("INSERT INTO movies (title, genre) VALUES (?, ?)", [
    ("Inception", "Sci-Fi"),
    ("Interstellar", "Sci-Fi"),
    ("The Dark Knight", "Action"),
    ("Titanic", "Drama"),
    ("Avatar", "Fantasy")
])

cur.executemany("INSERT INTO reviews (user_id, movie_id, rating) VALUES (?, ?, ?)", [
    (1, 1, 9),
    (2, 1, 8),
    (3, 2, 10),
    (4, 2, 9),
    (5, 3, 7),
    (1, 3, 8),
    (2, 4, 6),
    (3, 4, 7),
    (4, 5, 9),
    (5, 5, 8),
    (1, 5, 10)
])

# --- JOIN: имя пользователя + фильм + оценка ---
print("\nОтзывы пользователей:")
for row in cur.execute("""
SELECT u.name, m.title, r.rating
FROM reviews r
JOIN users u ON r.user_id = u.id
JOIN movies m ON r.movie_id = m.id
"""):
    print(row)

# --- JOIN: все фильмы (даже без отзывов) ---
print("\nВсе фильмы (с оценками, если есть):")
for row in cur.execute("""
SELECT m.title, r.rating
FROM movies m
LEFT JOIN reviews r ON m.id = r.movie_id
"""):
    print(row)

# --- Агрегации ---
print("\nАгрегации:")
cur.execute("SELECT AVG(rating), MAX(rating), MIN(rating) FROM reviews")
avg, max_r, min_r = cur.fetchone()
print(f"Средняя: {avg:.2f}, Макс: {max_r}, Мин: {min_r}")

conn.close()
