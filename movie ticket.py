import mysql.connector
from datetime import date
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="varad",       
        database="movie_booking"
    )


def create_tables():
    db = connect_db()
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies(
            MovieID INT PRIMARY KEY,
            Title VARCHAR(50),
            Genre VARCHAR(30),
            Duration INT,
            ShowTime VARCHAR(20),
            SeatsAvailable INT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Customers(
            CustomerID INT PRIMARY KEY,
            Name VARCHAR(50),
            Phone VARCHAR(15)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS Bookings(
            BookingID INT PRIMARY KEY,
            CustomerID INT,
            MovieID INT,
            NoOfTickets INT,
            BookingDate DATE,
            FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
            FOREIGN KEY (MovieID) REFERENCES Movies(MovieID)
        )
    """)

    db.commit()
    db.close()
    print("Tables created successfully.")

def add_movie():
    db = connect_db()
    cur = db.cursor()

    mid = int(input("Movie ID: "))
    title = input("Title: ")
    genre = input("Genre: ")
    duration = int(input("Duration (min): "))
    show = input("Show Time: ")
    seats = int(input("Seats Available: "))

    cur.execute("INSERT INTO Movies VALUES (%s, %s, %s, %s, %s, %s)",
                (mid, title, genre, duration, show, seats))

    db.commit()
    db.close()
    print("Movie added.")


def update_movie():
    db = connect_db()
    cur = db.cursor()

    mid = int(input("Enter Movie ID to update: "))
    field = input("Field to update (Title/Genre/Duration/ShowTime/SeatsAvailable): ")
    value = input("New Value: ")

    cur.execute(f"UPDATE Movies SET {field} = %s WHERE MovieID = %s", (value, mid))

    db.commit()
    db.close()
    print("Movie updated.")


def delete_movie():
    db = connect_db()
    cur = db.cursor()

    mid = int(input("Enter Movie ID to delete: "))
    cur.execute("DELETE FROM Movies WHERE MovieID = %s", (mid,))

    db.commit()
    db.close()
    print("Movie deleted.")

def user_register():
    db = connect_db()
    cur = db.cursor()

    cid = int(input("Customer ID: "))
    name = input("Name: ")
    phone = input("Phone: ")

    cur.execute("INSERT INTO Customers VALUES (%s, %s, %s)", (cid, name, phone))

    db.commit()
    db.close()
    print("Registration successful.")


def view_movies():
    db = connect_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM Movies")
    data = cur.fetchall()

    print("\n--- Available Movies ---")
    for m in data:
        print(f"ID:{m[0]} | {m[1]} | {m[2]} | {m[3]} mins | Time:{m[4]} | Seats:{m[5]}")

    db.close()


def book_ticket():
    db = connect_db()
    cur = db.cursor()

    cid = int(input("Enter Customer ID: "))
    mid = int(input("Enter Movie ID: "))

    # Check seats
    cur.execute("SELECT SeatsAvailable FROM Movies WHERE MovieID=%s", (mid,))
    result = cur.fetchone()

    if not result:
        print("Movie not found.")
        return

    seats = result[0]
    needed = int(input("How many tickets?: "))

    if needed > seats:
        print("Not enough seats.")
        return

    # Insert booking
    bid = int(input("Booking ID: "))
    cur.execute("INSERT INTO Bookings VALUES (%s, %s, %s, %s, %s)",
                (bid, cid, mid, needed, date.today()))

    # Update seats
    cur.execute("UPDATE Movies SET SeatsAvailable = SeatsAvailable - %s WHERE MovieID = %s",
                (needed, mid))

    db.commit()
    db.close()
    print("Booking successful.")


def view_user_bookings():
    db = connect_db()
    cur = db.cursor()

    cid = int(input("Enter Customer ID: "))
    cur.execute("""
        SELECT B.BookingID, M.Title, B.NoOfTickets, B.BookingDate
        FROM Bookings B
        JOIN Movies M ON B.MovieID = M.MovieID
        WHERE B.CustomerID = %s
    """, (cid,))

    data = cur.fetchall()

    print("\n--- Your Bookings ---")
    for b in data:
        print(f"BookingID:{b[0]} | Movie:{b[1]} | Tickets:{b[2]} | Date:{b[3]}")

    db.close()


def cancel_booking():
    db = connect_db()
    cur = db.cursor()

    bid = int(input("Enter Booking ID: "))

    cur.execute("SELECT MovieID, NoOfTickets FROM Bookings WHERE BookingID=%s", (bid,))
    result = cur.fetchone()

    if not result:
        print("Invalid booking.")
        return

    mid, tickets = result

    cur.execute("DELETE FROM Bookings WHERE BookingID=%s", (bid,))
    
    cur.execute("UPDATE Movies SET SeatsAvailable = SeatsAvailable + %s WHERE MovieID=%s",
                (tickets, mid))

    db.commit()
    db.close()
    print("Booking cancelled.")


def menu():
    while True:
        print("\n--- MENU ---")
        print("1. Add Movie")
        print("2. Update Movie")
        print("3. Delete Movie")
        print("4. Exit Admin")

        ch = int(input("Choice: "))

        if ch == 1:
            add_movie()
        elif ch == 2:
            update_movie()
        elif ch == 3:
            delete_movie()
        else:
            break


def user_menu():
    while True:
        print("\n--- USER MENU ---")
        print("1. Register")
        print("2. View Movies")
        print("3. Book Ticket")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Exit User")

        ch = int(input("Choice: "))

        if ch == 1:
            user_register()
        elif ch == 2:
            view_movies()
        elif ch == 3:
            book_ticket()
        elif ch == 4:
            view_user_bookings()
        elif ch == 5:
            cancel_booking()
        else:
            break
def main():
    while True:
        print("\n===== ONLINE MOVIE TICKET BOOKING SYSTEM =====")
        print("1. Admin Login")
        print("2. User Menu")
        print("3. Create Tables (Run Once)")
        print("4. Exit")

        ch = int(input("Choice: "))

        if ch == 1:
            password = input("Enter Admin Password: ")
            if password == "admin123":
                menu()
            else:
                print("Wrong password.")
        elif ch == 2:
            user_menu()
        elif ch == 3:
            create_tables()
        else:
            print("Exiting.")
            break


main()
