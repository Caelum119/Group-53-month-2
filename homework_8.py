import sqlite3

def create_connection(database_name):
    try:
        return sqlite3.connect(database_name)
    except sqlite3.Error as e:
        print(f"Connection error: {e}")
        return None

def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS countries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            area REAL DEFAULT 0,
            country_id INTEGER,
            FOREIGN KEY (country_id) REFERENCES countries(id)
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            city_id INTEGER,
            FOREIGN KEY (city_id) REFERENCES cities(id)
        );
    """)
    connection.commit()

def insert_country(connection, title):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM countries WHERE title = ?", (title,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO countries (title) VALUES (?)", (title,))
        connection.commit()

def insert_city(connection, title, area, country_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO cities (title, area, country_id) VALUES (?, ?, ?)", (title, area, country_id))
    connection.commit()

def insert_student(connection, first_name, last_name, city_id):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO students (first_name, last_name, city_id) VALUES (?, ?, ?)", (first_name, last_name, city_id))
    connection.commit()

def show_cities_menu(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id, title FROM cities")
    cities = cursor.fetchall()
    print("Вы можете отобразить список учеников по выбранному id города из перечня городов ниже, для выхода из программы введите 0:")
    for city in cities:
        print(f"{city[0]} - {city[1]}")
    return cities

def show_students_by_city(connection, city_id):
    cursor = connection.cursor()
    cursor.execute("""
        SELECT s.first_name, s.last_name, c.title, c.area, co.title
        FROM students s
        JOIN cities c ON s.city_id = c.id
        JOIN countries co ON c.country_id = co.id
        WHERE c.id = ?
    """, (city_id,))
    students = cursor.fetchall()
    for student in students:
        print(f"Имя: {student[0]}, Фамилия: {student[1]}, Город: {student[2]}, Площадь: {student[3]}, Страна: {student[4]}")

def seed_data(connection):
    insert_country(connection, 'Кыргызстан')
    insert_country(connection, 'Германия')
    insert_country(connection, 'Китай')

    insert_city(connection, 'Бишкек', 127.0, 1)
    insert_city(connection, 'Ош', 182.5, 1)
    insert_city(connection, 'Берлин', 891.8, 2)
    insert_city(connection, 'Мюнхен', 310.7, 2)
    insert_city(connection, 'Пекин', 16410.5, 3)
    insert_city(connection, 'Шанхай', 6340.5, 3)
    insert_city(connection, 'Тайван', 7400, 3)

    insert_student(connection, 'Айбек', 'Токтосунов', 1)
    insert_student(connection, 'Алина', 'Касымбеков', 1)
    insert_student(connection, 'Нурбек', 'Султанов', 2)
    insert_student(connection, 'Джон', 'Смит', 3)
    insert_student(connection, 'Арда', 'Гуллер', 3)
    insert_student(connection, 'Кайсер', 'Михаедь', 4)
    insert_student(connection, 'Ван', 'Ли', 5)
    insert_student(connection, 'Жу', 'Жу', 5)
    insert_student(connection, 'Тинг ', 'Ху', 6)
    insert_student(connection, 'Тайлунг', 'фй', 6)
    insert_student(connection, 'Кунгфу', 'Панда', 7)
    insert_student(connection, 'Айдана', 'Касымова', 2)
    insert_student(connection, 'Атай', 'Кайырдинов', 1)
    insert_student(connection, 'Фатима', 'Мамбетова', 4)
    insert_student(connection, 'Лейла', 'Жолдошбекова', 2)

def main():
    connection = create_connection('Hw_8.db')
    if connection:
        create_tables(connection)
        seed_data(connection)
        while True:
            cities = show_cities_menu(connection)
            try:
                selected_id = int(input("Введите id города: "))
                if selected_id == 0:
                    print("Выход из программы.")
                    break
                show_students_by_city(connection, selected_id)
            except ValueError:
                print("Пожалуйста, введите корректный номер.")

if __name__ == '__main__':
    main()
