from abc import ABC, abstractmethod

# --- Базовый класс героя ---
class Hero(ABC):
    def __init__(self, name, lvl, hp):
        self.name = name
        self.lvl = lvl
        self.hp = hp

    @abstractmethod
    def action(self):
        pass

    def __str__(self):
        return f"{self.name} | HP: {self.hp}"


# --- Наследник: Маг ---
class MageHero(Hero):
    def __init__(self, name, lvl, hp, mp):
        super().__init__(name, lvl, hp)
        self.mp = mp

    def action(self):
        print(f"Маг {self.name} кастует заклинание! MP: {self.mp}")


# --- Наследник: Воин (от MageHero) ---
class WarriorHero(MageHero):
    def __init__(self, name, lvl, hp, mp):
        super().__init__(name, lvl, hp, mp)

    def action(self):
        print(f"Воин {self.name} рубит мечом! Уровень: {self.lvl}")


# --- Класс банковского счёта ---
class BankAccount:
    bank_name = "Simba"

    def __init__(self, hero, balance, password):
        self.hero = hero
        self._balance = balance
        self.__password = password

    def login(self, password):
        return password == self.__password

    @property
    def full_info(self):
        return f"{self.hero.name} | Баланс: {self._balance} SOM"

    def get_bank_name(self):
        return BankAccount.bank_name

    def bonus_for_level(self):
        return self.hero.lvl * 10

    # --- Магические методы ---
    def __str__(self):
        return f"{self.hero.name} | Баланс: {self._balance} SOM"

    def __add__(self, other):
        if type(self.hero) is type(other.hero):
            return self._balance + other._balance
        else:
            return "Ошибка: Нельзя сложить счета героев разных классов!"

    def __eq__(self, other):
        return (type(self.hero) is type(other.hero)) and (self.hero.lvl == other.hero.lvl)


# --- Дополнительный класс SMS ---
class KGSms:
    def send_otp(self, phone):
        return f"Отправлен OTP на номер {phone}"


# --- Тестирование ---
mage1 = MageHero("Merlin", 50, 1000, 150)
warrior1 = WarriorHero("Conan", 50, 2000, 50)

acc1 = BankAccount(mage1, 5000, "1234")
acc2 = BankAccount(MageHero("Merlin", 50, 900, 150), 3000, "1234")
acc3 = BankAccount(warrior1, 7000, "4321")

# --- Вывод ---
mage1.action()
warrior1.action()

print(acc1)
print(acc2)

print("Банк:", acc1.get_bank_name())
print("Бонус за уровень:", acc1.bonus_for_level(), "SOM")

# --- __add__ ---
print("\n=== Проверка __add__ ===")
print("Сумма счетов двух магов:", acc1 + acc2)
print("Сумма мага и воина:", acc1 + acc3)

# --- __eq__ ---
print("\n=== Проверка __eq__ ===")
print("Mage1 == Mage2 ?", acc1 == acc2)
print("Mage1 == Warrior ?", acc1 == acc3)

# --- SMS ---
sms = KGSms()
print("\n", sms.send_otp("+996777123456"))
