from abc import ABC, abstractmethod

# --- Абстрактный класс Hero ---
class Hero(ABC):
    def __init__(self, name, level, strength, health):
        self.name = name
        self.level = level
        self.strength = strength
        self.__health = health   # приватный атрибут

    def greet(self):
        print(f"Привет, я {self.name}, мой уровень {self.level}")

    def rest(self):
        print(f"{self.name} отдыхает")
        self.__health += 1

    @abstractmethod
    def attack(self):
        pass

    # Дополнительно: метод для проверки здоровья
    def get_health(self):
        return self.__health


# --- Дочерние классы ---
class Warrior(Hero):
    def attack(self):
        print(f"Воин {self.name} атакует мечом!")


class Mage(Hero):
    def attack(self):
        print(f"Маг {self.name} использует магию!")


class Assassin(Hero):
    def attack(self):
        print(f"Ассасин {self.name} атакует из-под тишка!")


# --- Создание объектов ---
warrior = Warrior("Conan", 10, 15, 100)
mage = Mage("Merlin", 12, 8, 80)
assassin = Assassin("Ezio", 14, 12, 90)

# --- Вызов методов ---
for hero in (warrior, mage, assassin):
    hero.greet()
    hero.attack()
    hero.rest()
    print(f"Здоровье {hero.name}: {hero.get_health()}")
    print("------")
