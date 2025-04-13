import random
from decouple import Config, RepositoryIni

# Загружаем настройки из settings.ini
config = Config(repository=RepositoryIni('settings.ini'))

# Если настройки не найдены, используем значения по умолчанию
MIN_NUMBER = config.get('min_number', default=1, cast=int)
MAX_NUMBER = config.get('max_number', default=10, cast=int)
ATTEMPTS = config.get('attempts', default=5, cast=int)
CAPITAL = config.get('starting_capital', default=100, cast=int)

def play_game():
    secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
    capital = CAPITAL

    print(f"Угадай число от {MIN_NUMBER} до {MAX_NUMBER}. У тебя {ATTEMPTS} попыток.")

    for attempt in range(ATTEMPTS):
        print(f"\nПопытка {attempt + 1} из {ATTEMPTS}")
        guess = int(input("Введи число: "))
        bet = int(input("Ставка: "))

        # Проверяем, достаточно ли денег для ставки
        if bet > capital:
            print("У тебя нет столько денег! Попробуй уменьшить ставку.")
            continue  # Переходим к следующей попытке

        # Проверяем, угадал ли игрок
        if guess == secret_number:
            capital += bet  # Удваиваем ставку, если угадал
            print(f"🎉 Ты угадал! Теперь у тебя {capital} монет.")
            break
        else:
            capital -= bet  # Если не угадал, вычитаем ставку
            print(f"❌ Неправильно. Осталось {capital} монет.")

    # После окончания игры показываем результат
    print(f"\nИгра окончена. Загаданное число было: {secret_number}")
