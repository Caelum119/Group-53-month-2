import sqlite3

def create_connection(database_name):
    try:
        return sqlite3.connect(database_name)
    except sqlite3.Error as e:
        print(f"Error creating connection: {e}")
        return None

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        );
    """)
    connection.commit()

def insert_product(connection, title, price, quantity):
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM products WHERE title = ?", (title,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO products (title, price, quantity) VALUES (?, ?, ?)", (title, price, quantity))
        connection.commit()
    else:
        print(f"Product '{title}' already exists.")

def update_quantity_by_id(connection, product_id, new_quantity):
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id))
    connection.commit()

def update_price_by_id(connection, product_id, new_price):
    cursor = connection.cursor()
    cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
    connection.commit()

def delete_product_by_id(connection, product_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
    connection.commit()

def select_all_products(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def select_products_by_price_and_quantity(connection, max_price, min_quantity):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE price < ? AND quantity > ?", (max_price, min_quantity))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def search_product_by_title(connection, search_term):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM products WHERE title LIKE ?", ('%' + search_term + '%',))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def add_products(connection):
    insert_product(connection, 'iPhone 15 Pro Max', 1899, 10)
    insert_product(connection, 'iPhone 15', 1399, 15)
    insert_product(connection, 'iPhone 14', 1199, 8)
    insert_product(connection, 'iPhone 13', 999, 20)
    insert_product(connection, 'iPhone SE', 799, 30)
    insert_product(connection, 'AirPods Pro 2', 299, 25)
    insert_product(connection, 'MacBook Pro M3', 2499, 5)
    insert_product(connection, 'MacBook Air M2', 1499, 12)
    insert_product(connection, 'iPad Pro 12.9', 1299, 7)
    insert_product(connection, 'iPad Mini', 599, 10)
    insert_product(connection, 'Apple Watch Ultra 2', 999, 4)
    insert_product(connection, 'Apple Watch SE', 399, 20)
    insert_product(connection, 'Magic Keyboard', 149, 13)
    insert_product(connection, 'Apple TV 4K', 179, 9)
    insert_product(connection, 'HomePod Mini', 99, 16)

def test_functions():
    database_name = 'hw.db'
    my_connection = create_connection(database_name)

    if my_connection:
        create_table(my_connection)
        add_products(my_connection)
        update_quantity_by_id(my_connection, 1, 50)
        update_price_by_id(my_connection, 1, 1800)
        delete_product_by_id(my_connection, 2)
        select_all_products(my_connection)
        select_products_by_price_and_quantity(my_connection, 1000, 10)
        search_product_by_title(my_connection, "iPhone")
        my_connection.close()



test_functions()

