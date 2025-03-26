PRAGMA foreign_keys = OFF;

-- DROP TABLE IF EXISTS FinePayments;
-- DROP TABLE IF EXISTS EventRegistrations;
-- DROP TABLE IF EXISTS Volunteers;
-- DROP TABLE IF EXISTS LibraryPersonnel;
-- DROP TABLE IF EXISTS Events;
-- DROP TABLE IF EXISTS FutureItems;
-- DROP TABLE IF EXISTS Borrowing;
-- DROP TABLE IF EXISTS LibraryUsers;
-- DROP TABLE IF EXISTS LibraryItems;
-- DROP TABLE IF EXISTS HelpRequests;
-- DROP TABLE IF EXISTS Rooms;

PRAGMA foreign_keys = ON;

-- Library Items Table
CREATE TABLE LibraryItems (
    ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Author TEXT,
    ItemType TEXT CHECK(ItemType IN ('printBooks','onlineBooks','magazines','scientificJournals','cds','records','other')),
    PublicationDate DATE,
    AvailableCopies INTEGER NOT NULL CHECK(AvailableCopies >= 0),
    Status TEXT CHECK(Status IN ('Available', 'Borrowed', 'Reserved')) DEFAULT 'Available'
);

-- Library Users Table
CREATE TABLE LibraryUsers (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT UNIQUE NOT NULL,
    Phone TEXT NOT NULL,
    MembershipDate DATE DEFAULT CURRENT_DATE,
    TotalFines DECIMAL(10,2) DEFAULT 0.00 CHECK(TotalFines >= 0)
);

-- Borrowing Transactions
CREATE TABLE Borrowing (
    TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    ItemID INTEGER NOT NULL,
    BorrowDate DATE DEFAULT CURRENT_DATE,
    DueDate DATE NOT NULL,
    ReturnDate DATE,
    FOREIGN KEY(UserID) REFERENCES LibraryUsers(UserID),
    FOREIGN KEY(ItemID) REFERENCES LibraryItems(ItemID),
    CHECK (ReturnDate IS NULL OR ReturnDate >= BorrowDate)
);

-- Fine Payments
CREATE TABLE FinePayments (
    PaymentID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    Amount DECIMAL(10,2) NOT NULL CHECK(Amount > 0),
    PaymentDate DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY(UserID) REFERENCES LibraryUsers(UserID)
);

-- Events Table
CREATE TABLE Events (
    EventID INTEGER PRIMARY KEY AUTOINCREMENT,
    EventName TEXT NOT NULL,
    EventDate DATE NOT NULL,
    EventType TEXT CHECK(EventType IN ('BookClub','BookEvent','ArtShow','FilmScreening','Other')),
    Audience TEXT CHECK(Audience IN ('Babies','Toddlers','Kids','Tweens','Teens','Adults','AllAges')),
    RoomID INTEGER NOT NULL,
    FOREIGN KEY(RoomID) REFERENCES Rooms(RoomID)
);

-- Event Registrations
CREATE TABLE EventRegistrations (
    RegistrationID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    EventID INTEGER NOT NULL,
    FOREIGN KEY(UserID) REFERENCES LibraryUsers(UserID),
    FOREIGN KEY(EventID) REFERENCES Events(EventID),
    UNIQUE(UserID, EventID)
);

CREATE TABLE Rooms (
    RoomID INTEGER PRIMARY KEY AUTOINCREMENT,
    RoomNumber INTEGER NOT NULL UNIQUE,
    Capacity INTEGER NOT NULL CHECK(Capacity > 0),
    Location TEXT NOT NULL
);

CREATE TABLE LibraryPersonnel (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Position TEXT CHECK(Position IN ('Librarian', 'Administrator', 'Volunteer', 'Maintenance')),
    Email TEXT UNIQUE NOT NULL,
    Phone TEXT NOT NULL
);

CREATE TABLE Volunteers (
    VolunteerID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    Role TEXT CHECK(Role IN ('General', 'Event Helper', 'Book Sorting', 'Other')),
    StartDate DATE NOT NULL,
    FOREIGN KEY(UserID) REFERENCES LibraryUsers(UserID)
);

CREATE TABLE HelpRequests (
    RequestID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER NOT NULL,
    StaffID INTEGER NOT NULL,
    RequestText TEXT NOT NULL,
    RequestDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    Status TEXT CHECK(Status IN ('Open', 'Resolved')) DEFAULT 'Open',
    FOREIGN KEY(UserID) REFERENCES LibraryUsers(UserID),
    FOREIGN KEY(StaffID) REFERENCES LibraryPersonnel(StaffID)
);

CREATE TABLE FutureItems (
    FutureItemID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title VARCHAR(255) NOT NULL,
    AuthorCreator VARCHAR(255),
    ExpectedArrivalDate DATE NOT NULL,
    Status VARCHAR(255) CHECK(Status IN ('Pending','Ordered')),
    LibraryItemID INTEGER UNIQUE,
    FOREIGN KEY(LibraryItemID) REFERENCES LibraryItems(ItemID) ON DELETE SET NULL
);


-- Triggers
CREATE TRIGGER UpdateBorrowStatus
AFTER INSERT ON Borrowing
BEGIN
    UPDATE LibraryItems
    SET AvailableCopies = AvailableCopies - 1,
        Status = CASE 
            WHEN AvailableCopies - 1 > 0 THEN 'Available' 
            ELSE 'Borrowed' 
        END
    WHERE ItemID = NEW.ItemID;
END;

CREATE TRIGGER UpdateReturnStatus
AFTER UPDATE OF ReturnDate ON Borrowing
WHEN NEW.ReturnDate IS NOT NULL
BEGIN
    UPDATE LibraryItems
    SET AvailableCopies = AvailableCopies + 1,
        Status = CASE 
            WHEN AvailableCopies + 1 > 0 THEN 'Available' 
            ELSE 'Borrowed' 
        END
    WHERE ItemID = NEW.ItemID;
    
    UPDATE LibraryUsers
    SET TotalFines = TotalFines + 
        (CASE 
            WHEN julianday(NEW.ReturnDate) > julianday(NEW.DueDate)
            THEN (julianday(NEW.ReturnDate) - julianday(NEW.DueDate)) * 0.50
            ELSE 0 
        END)
    WHERE UserID = NEW.UserID;
END;

CREATE TRIGGER ConvertFutureItem 
AFTER UPDATE OF Status ON FutureItems
WHEN NEW.Status = 'Ordered' AND NEW.LibraryItemID IS NULL
BEGIN
    INSERT INTO LibraryItems (Title, Author, ItemType, AvailableCopies)
    VALUES (NEW.Title, NEW.AuthorCreator, 'other', 0);
    
    UPDATE FutureItems 
    SET LibraryItemID = last_insert_rowid() 
    WHERE FutureItemID = NEW.FutureItemID;
END;