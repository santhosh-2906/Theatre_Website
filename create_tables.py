from config.db import get_db_connection

def create_users_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    )
    """)

def create_movies_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        duration VARCHAR(20),
        poster_url VARCHAR(255),
        release_date DATE
    )
    """)

def create_screens_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Screens (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        capacity INT
    )
    """)

def create_shows_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Shows (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT,
        screen_id INT,
        show_time DATETIME,
        price DECIMAL(10,2),
        FOREIGN KEY (movie_id) REFERENCES Movies(id),
        FOREIGN KEY (screen_id) REFERENCES Screens(id)
    )
    """)

def create_snacks_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Snacks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        price DECIMAL(10,2)
    )
    """)

def create_bookings_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        show_id INT,
        seat_number VARCHAR(10),
        booking_time DATETIME,
        snack_id INT,
        FOREIGN KEY (user_id) REFERENCES Users(id),
        FOREIGN KEY (show_id) REFERENCES Shows(id),
        FOREIGN KEY (snack_id) REFERENCES Snacks(id)
    )
    """)

def main():
    conn = get_db_connection()
    cursor = conn.cursor()

   
    create_users_table(cursor)
    create_movies_table(cursor)
    create_screens_table(cursor)
    create_shows_table(cursor)
    create_snacks_table(cursor)
    create_bookings_table(cursor)

   
    conn.commit()
    cursor.close()
    conn.close()

    print("All tables created successfully!")

if __name__ == "__main__":
    main()
