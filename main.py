import mysql.connector
from mysql.connector import Error

config = {
    "user": "my_username",
    "password": "my_password",
    "host": "localhost",
    "database": "library_management_db"
}

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Query executed successfully!")
    except Error as e:
        print(f"The error '{e}' occurred!")

def fetch_results(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred!")
    return result

def main_menu():
    while True:
        print('\nMain Menu:')
        print('1. Book Operations')
        print('2. User Operations')
        print('3. Author Operations')
        print("4. Quit")

        choice = input("Enter your choice: ")
        if choice == "1":
            book_operations()
        elif choice == "2":
            user_operations()
        elif choice == "3":
            author_operations()
        elif choice == "4":
            print("Quiting the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again!")

def book_operations():
    while True:
        print('\nBook Operations:')
        print('1. Add a new book')
        print('2. Borrow a book')
        print('3. Return a book')
        print('4. Search for a book')
        print('5. Display all books')
        print('6. Back to Main Menu')

        choice = input("Enter your choice:")
        if choice == "1":
            add_book()
        elif choice == "2":
            borrow_book()
        elif choice == "3":
            return_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            display_books()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again!")

def user_operations():
    while True:
        print('\nUser Operations:')
        print('1. Add a new user')
        print('2. View user details')
        print('3. Display all users')
        print('4. Back to Main Menu')

        choice = input("Enter your choice: ")
        if choice == "1":
            add_user()
        elif choice == "2":
            view_user()
        elif choice == "3":
            display_users()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again!")

def author_operations():
    while True:
        print('\nAuthor Operations:')
        print('1. Add a new author')
        print('2. View author details')
        print('3. Display all authors')
        print('4. Back to Main Menu')

        choice = input("Enter your choice: ")
        if choice == "1":
            add_author()
        elif choice == "2":
            view_author()
        elif choice == "3":
            display_authors()
        elif choice == "4":
            break
        else:
            print("Invalid choice. Please try again!")

def add_book():
    connection = create_connection()
    title = input("Enter book title: ")
    author_id = int(input("Enter author ID: "))
    isbn = input("Enter ISBN: ")
    publication_date = input("Enter publication date (YYYY-MM-DD): ")
    query = """
    INSERT INTO books (title, author_id, isbn, publication_date) VALUES (%s, %s, %s, %s)
    """
    data = (title, author_id, isbn, publication_date)
    execute_query(connection, query, data)
    connection.close()

def borrow_book():
    connection = create_connection()
    user_id = int(input("Enter user ID: "))
    book_id = int(input("Enter book ID: "))
    borrow_date = input("Enter borrow date (YYYY-MM-DD): ")
    query = """
    INSERT INTO borrowed_books (user_id, book_id, borrow_date) VALUES (%s, %s, %s)
    """
    data = (user_id, book_id, borrow_date)
    execute_query(connection, query, data)
    update_query = """
    UPDATE books SET availability = 0 WHERE id = %s
    """
    execute_query(connection, update_query, (book_id,))
    connection.close()

def return_book():
    connection = create_connection()
    book_id = int(input("Enter book ID: "))
    return_date = input("Enter return date (YYYY-MM-DD): ")
    query = """
    UPDATE borrowed_books SET return_date = %s WHERE book_id = %s AND return_date IS NULL
    """
    data = (return_date, book_id)
    execute_query(connection, query, data)
    update_query = """
    UPDATE books SET availability = 1 WHERE id = %s
    """
    execute_query(connection, update_query, (book_id,))
    connection.close()

def search_book():
    connection = create_connection()
    title = input("Enter book title to search: ")
    query = f"""
    SELECT * FROM books WHERE title LIKE '%{title}%'
    """
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

def display_books():
    connection = create_connection()
    query = "SELECT * FROM books"
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

def add_user():
    connection = create_connection()
    name = input("Enter user name: ")
    library_id = input("Enter library ID: ")
    query = """
    INSERT INTO users (name, library_id) VALUES (%s, %s)
    """
    data = (name, library_id)
    execute_query(connection, query, data)
    connection.close()

def view_user():
    connection = create_connection()
    user_id = int(input("Enter user ID: "))
    query = f"SELECT * FROM users WHERE id = {user_id}"
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

def display_users():
    connection = create_connection()
    query = "SELECT * FROM users"
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

def add_author():
    connection = create_connection()
    name = input("Enter author name: ")
    biography = input("Enter author biography: ")
    query = """
    INSERT INTO authors (name, biography) VALUES (%s, %s)
    """
    data = (name, biography)
    execute_query(connection, query, data)
    connection.close()

def view_author():
    connection = create_connection()
    author_id = int(input("Enter author ID: "))
    query = f"SELECT * FROM authors WHERE id = {author_id}"
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

def display_authors():
    connection = create_connection()
    query = "SELECT * FROM authors"
    results = fetch_results(connection, query)
    for row in results:
        print(row)
    connection.close()

if __name__ == "__main__":
    main_menu()