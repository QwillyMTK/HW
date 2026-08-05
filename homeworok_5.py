import time

# --- Задание 1: Проверка администратора ---
class User:
    def __init__(self, name, role):
        self.name = name
        self.role = role


def is_admin(func):
    def wrapper(user, *args, **kwargs):
        if user.role == "admin":
            return func(user, *args, **kwargs)
        else:
            print("У вас нет доступа")
    return wrapper


@is_admin
def delete_video(user):
    print("Видео удалено")


# --- Задание 2: Декоратор таймера ---
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Время выполнения: {round(end - start, 2)} секунд")
        return result
    return wrapper


@timer
def download_video():
    time.sleep(2)
    print("Видео загружено")


# --- Тестирование ---
admin = User("Ardager", "admin")
user = User("Bek", "user")

delete_video(admin)  # должно удалить
delete_video(user)   # должно отказать

download_video()     # должно показать задержку и время
