import sqlite3

def create_connection(database_name):
    try:
        return sqlite3.connect(database_name)
    except sqlite3.Error as e:
        print(f"Connection error: {e}")
        return None

def create_tables(connection):
    cursor = connection.cursor()
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS categories (
        code TEXT PRIMARY KEY,
        title TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS stores (
        store_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category_code TEXT NOT NULL,
        unit_price REAL NOT NULL,
        stock_quantity INTEGER NOT NULL,
        store_id INTEGER NOT NULL,
        FOREIGN KEY (category_code) REFERENCES categories(code),
        FOREIGN KEY (store_id) REFERENCES stores(store_id)
    );
    """)
    connection.commit()

def insert_initial_data(connection):
    cursor = connection.cursor()
    cursor.execute("INSERT OR IGNORE INTO categories (code, title) VALUES ('FD', 'Food products'), ('EL', 'Electronics')")
    cursor.execute("INSERT OR IGNORE INTO stores (store_id, title) VALUES (1, 'Asia'), (2, 'Globus'), (3, 'Spar')")
    products = [
        ("Alpen_gold", "FD", 120, 150, 1),
        ("Lays", "FD", 140, 80, 2),
        ("TV", "EL", 550.0, 10, 3),
        ("Bread", "FD", 2.5, 50, 1),
        ("Smartphone", "EL", 800, 15, 2),
        ("Vacuum_cleaner", "EL", 400, 6, 1)



    ]
    for title, code, price, qty, store_id in products:
        cursor.execute("SELECT id FROM products WHERE title = ? AND store_id = ?", (title, store_id))
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO products (title, category_code, unit_price, stock_quantity, store_id) VALUES (?, ?, ?, ?, ?)",
                           (title, code, price, qty, store_id))
    connection.commit()

def list_stores(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT store_id, title FROM stores")
    return cursor.fetchall()

def display_products_by_store(connection, store_id):
    cursor = connection.cursor()
    cursor.execute("""
    SELECT p.title, c.title, p.unit_price, p.stock_quantity
    FROM products p
    JOIN categories c ON p.category_code = c.code
    WHERE p.store_id = ?
    """, (store_id,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"\nНазвание продукта: {row[0]}")
            print(f"Категория: {row[1]}")
            print(f"Цена: {row[2]}")
            print(f"Количество на складе: {row[3]}")
    else:
        print("Нет продуктов в этом магазине.")

def run_program():
    database_name = "Additional_lesson1.db"
    connection = create_connection(database_name)
    if connection:
        create_tables(connection)
        insert_initial_data(connection)
        while True:
            print("\nВы можете отобразить список продуктов по выбранному id магазина из перечня магазинов ниже, для выхода из программы введите цифру 0:")
            stores = list_stores(connection)
            for store in stores:
                print(f"{store[0]}. {store[1]}")
            try:
                choice = int(input("Введите ID магазина: "))
                if choice == 0:
                    print("Выход из программы.")
                    break
                display_products_by_store(connection, choice)
            except ValueError:
                print("Введите корректный ID.")
        connection.close()

run_program()
