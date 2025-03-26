import sqlite3
from datetime import date, timedelta
def populate_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # ====================
    # 1. Rooms (10 entries)
    # ====================
    rooms = [
        (101, 50, 'Main Building Floor 1'),
        (102, 30, 'Main Building Floor 1'),
        (103, 25, 'Main Building Floor 2'),
        (201, 100, 'Annex Building Auditorium'),
        (202, 20, 'Annex Building Study Room'),
        (203, 15, 'Annex Building Childrens Corner'),
        (301, 40, 'East Wing Media Center'),
        (302, 10, 'East Wing Quiet Zone'),
        (401, 200, 'West Wing Event Hall'),
        (501, 30, 'West Wing Seminar Room')
    ]
    c.executemany("INSERT INTO Rooms (RoomNumber, Capacity, Location) VALUES (?, ?, ?)", rooms)

    # ========================
    # 2. Library Items (15 entries)
    # ========================
    items = [
        ('The Hobbit', 'J.R.R. Tolkien', 'printBooks', 3),
        ('Harry Potter 1', 'J.K. Rowling', 'printBooks', 5),
        ('National Geographic 2023', None, 'magazines', 10),
        ('Python Crash Course', 'Eric Matthes', 'onlineBooks', 2),
        ('Mona Lisa CD', 'Leonardo da Vinci', 'cds', 1),
        ('Space Exploration Journal', 'NASA', 'scientificJournals', 2),
        ('Baby Shark CD', 'Pinkfong', 'cds', 3),
        ('Learn Spanish', 'Language Experts', 'records', 2),
        ('Art History Today', 'Museum Press', 'magazines', 4),
        ('The Little Prince', 'Antoine de Saint-Exupéry', 'printBooks', 1),
        ('SQL Fundamentals', 'Alice Smith', 'onlineBooks', 3),
        ('Modern Art Review', None, 'magazines', 5),
        ('Classical Music Collection', 'Vienna Philharmonic', 'cds', 2),
        ('AI Research Papers', 'DeepMind', 'scientificJournals', 1),
        ('French Language Basics', 'Language Experts', 'records', 3)
    ]
    c.executemany("""
        INSERT INTO LibraryItems (Title, Author, ItemType, AvailableCopies)
        VALUES (?, ?, ?, ?)
    """, items)

    # ========================
    # 3. Library Users (15 entries)
    # ========================
    users = [
        ('Alice Wonder', 'alice@email.com', '555-0101'),
        ('Bob Builder', 'bob@email.com', '555-0102'),
        ('Charlie Brown', 'charlie@email.com', '555-0103'),
        ('Diana Prince', 'diana@email.com', '555-0104'),
        ('Ethan Hunt', 'ethan@email.com', '555-0105'),
        ('Fiona Apple', 'fiona@email.com', '555-0106'),
        ('George Jetson', 'george@email.com', '555-0107'),
        ('Hannah Montana', 'hannah@email.com', '555-0108'),
        ('Ian Fleming', 'ian@email.com', '555-0109'),
        ('Julia Child', 'julia@email.com', '555-0110'),
        ('Kevin Hart', 'kevin@email.com', '555-0111'),
        ('Lisa Simpson', 'lisa@email.com', '555-0112'),
        ('Mike Tyson', 'mike@email.com', '555-0113'),
        ('Nina Patel', 'nina@email.com', '555-0114'),
        ('Oscar Wilde', 'oscar@email.com', '555-0115')
    ]
    c.executemany("INSERT INTO LibraryUsers (Name, Email, Phone) VALUES (?, ?, ?)", users)

    # =============================
    # 4. Library Personnel (10 entries)
    # =============================
    personnel = [
        ('Sarah Connor', 'Librarian', 'sarah@library.com', '555-0200'),
        ('John Smith', 'Administrator', 'john@library.com', '555-0201'),
        ('Emily Davis', 'Librarian', 'emily@library.com', '555-0202'),
        ('Michael Brown', 'Maintenance', 'michael@library.com', '555-0203'),
        ('Laura Wilson', 'Volunteer', 'laura@library.com', '555-0204'),
        ('David Lee', 'Volunteer', 'david@library.com', '555-0205'),
        ('Sophia Martinez', 'Librarian', 'sophia@library.com', '555-0206'),
        ('James Anderson', 'Volunteer', 'james@library.com', '555-0207'),
        ('Emma Taylor', 'Volunteer', 'emma@library.com', '555-0208'),
        ('Daniel Clark', 'Librarian', 'daniel@library.com', '555-0209')
    ]
    c.executemany("INSERT INTO LibraryPersonnel (Name, Position, Email, Phone) VALUES (?, ?, ?, ?)", personnel)

    # ======================
    # 5. Events (15 entries)
    # ======================
    events = [
        ('Kids Story Hour', '2026-12-01', 'BookClub', 'Kids', 3),
        ('Python Workshop', '2026-12-05', 'BookEvent', 'Adults', 4),
        ('Art Exhibition', '2026-12-10', 'ArtShow', 'AllAges', 9),
        ('Movie Night: Toy Story', '2026-12-15', 'FilmScreening', 'AllAges', 9),
        ('Teen Book Club', '2026-12-20', 'BookClub', 'Teens', 5),
        ('Baby Music Time', '2026-12-03', 'Other', 'Babies', 3),
        ('Science Journal Reading', '2026-12-08', 'BookEvent', 'Adults', 6),
        ('CD Listening Party', '2026-12-12', 'Other', 'AllAges', 7),
        ('Author Meet & Greet', '2026-12-18', 'BookEvent', 'Adults', 10),
        ('Magazine Swap', '2026-12-22', 'Other', 'AllAges', 9),
        ('Winter Book Sale', '2026-12-24', 'Other', 'AllAges', 9),
        ('Holiday Crafts', '2026-12-14', 'ArtShow', 'Kids', 3),
        ('Career Workshop', '2026-01-05', 'BookEvent', 'Adults', 4),
        ('Genealogy Research', '2026-01-12', 'Other', 'Adults', 8),
        ('Poetry Night', '2026-01-19', 'BookClub', 'Teens', 5)
    ]
    c.executemany("""
        INSERT INTO Events (EventName, EventDate, EventType, Audience, RoomID)
        VALUES (?, ?, ?, ?, ?)
    """, events)

    # ========================
    # 6. Borrowing (15 entries)
    # ========================
    borrowing = [
        (1, 1, '2023-11-01', '2023-11-15', '2023-11-14'),
        (2, 2, '2023-11-02', '2023-11-16', '2023-11-20'),
        (3, 3, '2023-11-03', '2023-11-17', None),
        (4, 4, '2023-11-04', '2023-11-18', '2023-11-25'),
        (5, 5, '2023-11-05', '2023-11-19', '2023-11-18'),
        (6, 6, '2023-11-06', '2023-11-20', None),
        (7, 7, '2023-11-07', '2023-11-21', '2023-11-22'),
        (8, 8, '2023-11-08', '2023-11-22', '2023-11-21'),
        (9, 9, '2023-11-09', '2023-11-23', None),
        (10, 10, '2023-11-10', '2023-11-24', '2023-11-25'),
        (11, 11, '2023-11-11', '2023-11-25', '2023-11-24'),
        (12, 12, '2023-11-12', '2023-11-26', None),
        (13, 13, '2023-11-13', '2023-11-27', '2023-11-28'),
        (14, 14, '2023-11-14', '2023-11-28', None),
        (15, 15, '2023-11-15', '2023-11-29', '2023-11-28')
    ]
    c.executemany("""
        INSERT INTO Borrowing (UserID, ItemID, BorrowDate, DueDate, ReturnDate)
        VALUES (?, ?, ?, ?, ?)
    """, borrowing)

    # ============================
    # 7. Event Registrations (15 entries)
    # ============================
    registrations = [
        (1, 1), (2, 1), (3, 1), (4, 2), (5, 2),
        (6, 3), (7, 4), (8, 5), (9, 6), (10, 7),
        (11, 8), (12, 9), (13, 10), (14, 11), (15, 12)
    ]
    c.executemany("INSERT INTO EventRegistrations (UserID, EventID) VALUES (?, ?)", registrations)

    # ======================
    # 8. Volunteers (15 entries)
    # ======================
    volunteers = [
        (1, 'Event Helper', '2023-01-15'),
        (2, 'Book Sorting', '2023-02-01'),
        (3, 'General', '2023-03-10'),
        (4, 'Other', '2023-04-22'),
        (5, 'Event Helper', '2023-05-05'),
        (6, 'Book Sorting', '2023-06-18'),
        (7, 'General', '2023-07-01'),
        (8, 'Other', '2023-08-14'),
        (9, 'Event Helper', '2023-09-27'),
        (10, 'Book Sorting', '2023-10-10'),
        (11, 'General', '2023-11-23'),
        (12, 'Other', '2023-12-05'),
        (13, 'Event Helper', '2024-01-08'),
        (14, 'Book Sorting', '2024-02-11'),
        (15, 'General', '2024-03-15')
    ]
    c.executemany("INSERT INTO Volunteers (UserID, Role, StartDate) VALUES (?, ?, ?)", volunteers)

    # =========================
    # 9. Help Requests (15 entries)
    # =========================
    help_requests = [
        (1, 1, "Can't find book in catalog", 'Open'),
        (2, 2, "Computer not working", 'Resolved'),
        (3, 3, "Need research assistance", 'Open'),
        (4, 4, "Printer jammed", 'Resolved'),
        (5, 5, "Request book purchase", 'Open'),
        (6, 6, "Event room too cold", 'Resolved'),
        (7, 7, "Missing library card", 'Open'),
        (8, 8, "Wi-Fi connection issues", 'Resolved'),
        (9, 9, "Interlibrary loan request", 'Open'),
        (10, 10, "Donation inquiry", 'Resolved'),
        (11, 1, "Study room reservation", 'Open'),
        (12, 2, "Database access problem", 'Resolved'),
        (13, 3, "Citation help needed", 'Open'),
        (14, 4, "Light fixture broken", 'Resolved'),
        (15, 5, "Book renewal request", 'Open')
    ]
    c.executemany("""
        INSERT INTO HelpRequests (UserID, StaffID, RequestText, Status)
        VALUES (?, ?, ?, ?)
    """, help_requests)

    # =========================
    # 10. Future Items (15 entries)
    # =========================
    future_items = [
        ('Advanced Python', 'Eric Matthes', '2024-06-01', 'Pending', None),
        ('Mars Exploration Guide', 'NASA', '2024-07-15', 'Ordered', 14),
        ('Modern Art Vol. 2', 'Museum Press', '2024-08-30', 'Pending', None),
        ('Spanish Conversation', 'Language Experts', '2024-09-10', 'Ordered', 15),
        ('Quantum Physics Journal', 'CERN', '2024-10-05', 'Pending', None),
        ('Classic Rock Anthology', 'Rolling Stone', '2024-11-20', 'Ordered', 13),
        ('AI Ethics Papers', 'DeepMind', '2025-01-15', 'Pending', None),
        ('Childrens Science Series', 'NatGeo Kids', '2025-02-28', 'Ordered', 12),
        ('French Literature Classics', 'Paris Press', '2025-03-10', 'Pending', None),
        ('Space Opera Collection', 'Sci-Fi Authors', '2025-04-22', 'Ordered', 11),
        ('Advanced SQL Techniques', 'Alice Smith', '2025-05-05', 'Pending', None),
        ('Music Theory Guide', 'Berkeley Music', '2025-06-18', 'Ordered', 10),
        ('Modern Architecture', 'Frank Lloyd Wright', '2025-07-01', 'Pending', None),
        ('World History Encyclopedia', 'Historians Inc', '2025-08-14', 'Ordered', 9),
        ('Advanced Robotics', 'MIT Press', '2025-09-27', 'Pending', None)
    ]
    c.executemany("""
        INSERT INTO FutureItems (Title, AuthorCreator, ExpectedArrivalDate, Status, LibraryItemID)
        VALUES (?, ?, ?, ?, ?)
    """, future_items)

    # =========================
    # 11. Fine Payments (15 entries)
    # =========================
    fine_payments = [
        (2, 2.50, '2023-11-21'),
        (4, 3.75, '2023-11-26'),
        (7, 1.25, '2023-11-23'),
        (10, 2.00, '2023-11-26'),
        (13, 4.50, '2023-11-29'),
        (2, 1.00, '2023-11-28'),
        (4, 2.25, '2023-11-29'),
        (7, 0.75, '2023-11-25'),
        (10, 1.50, '2023-11-27'),
        (13, 3.00, '2023-11-30'),
        (2, 0.50, '2023-11-30'),
        (4, 1.75, '2023-12-01'),
        (7, 0.25, '2023-12-02'),
        (10, 1.00, '2023-12-03'),
        (13, 2.50, '2023-12-04')
    ]
    c.executemany("INSERT INTO FinePayments (UserID, Amount, PaymentDate) VALUES (?, ?, ?)", fine_payments)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_database()
    print("Database populated with 15+ entries per table!")