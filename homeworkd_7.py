import sqlite3

# Подключение к базе данных (если файла нет — создастся автоматически)
connect = sqlite3.connect('store.db')
cursor = connect.cursor()

# Создание таблицы products
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        quantity INTEGER NOT NULL
    )
''')
connect.commit()


# CREATE — добавление товара
def create_product(name, price, quantity):
    cursor.execute(
        'INSERT INTO products(name, price, quantity) VALUES(?,?,?)',
        (name, price, quantity)
    )
    connect.commit()
    print(f"✅ Товар '{name}' добавлен!")


# READ — получение всех товаров
def read_products():
    cursor.execute('SELECT * FROM products')
    data = cursor.fetchall()
    for row in data:
        print(row)


# UPDATE — обновление цены по id
def update_product(id, price):
    cursor.execute(
        'UPDATE products SET price = ? WHERE id = ?',
        (price, id)
    )
    connect.commit()
    print(f"🔄 Цена товара с id={id} обновлена!")


# DELETE — удаление товара по id
def delete_product(id):
    cursor.execute(
        'DELETE FROM products WHERE id = ?',
        (id,)
    )
    connect.commit()
    print(f"❌ Товар с id={id} удалён!")


# --- Пример использования ---
if __name__ == "__main__":
    # Добавляем товары
    create_product("Ноутбук", 55000, 10)
    create_product("Смартфон", 30000, 25)

    # Читаем все товары
    print("\n📦 Список товаров:")
    read_products()

    # Обновляем цену
    update_product(1, 60000)

    # Удаляем товар
    delete_product(2)

    print("\n📦 Итоговый список:")
    read_products()
