import sqlite3
from datetime import datetime, timedelta
import sys

class LibrarySystem:
    def __init__(self, db_name='library.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

    # Helper Methods
    def clear_screen(self):
        print("\n" * 3)
        
    def press_enter(self):
        input("\nPress Enter to continue...")

    def _get_valid_input(self, prompt, valid_options):
        """Helper method to validate user input against allowed options"""
        while True:
            user_input = input(prompt).strip()
            if user_input in valid_options:
                return user_input
            print(f"Invalid option! Must be one of: {', '.join(valid_options)}")

    # Search Feature
    def search_items(self):
        self.clear_screen()
        print("🔍 Search Library Items 🔍")
        term = input("Enter title/author (or leave blank to see all): ").strip()
        query = """
            SELECT * FROM LibraryItems 
            WHERE Title LIKE ? OR Author LIKE ?
            ORDER BY AvailableCopies DESC
        """
        search_term = f"%{term}%" if term else "%"
        
        try:
            items = self.conn.execute(query, (search_term, search_term)).fetchall()
            if not items:
                print("\nNo items found 😞")
                return
                
            print("\n📚 Search Results:")
            for item in items:
                print(f"""
                ID: {item['ItemID']}
                Title: {item['Title']}
                Author: {item['Author'] or 'Unknown'}
                Type: {item['ItemType']}
                Available: {item['AvailableCopies']}
                Status: {item['Status']}
                """)
                
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")

    # User Authentication
    def get_user_id(self):
        self.clear_screen()
        while True:
            print("🔐 Please login first 🔐")
            print("1. I have a User ID")
            print("2. Register as new user")
            print("3. Go back")
            
            choice = input("Choose (1-3): ")
            
            if choice == '1':
                user_id = input("Enter your User ID: ")
                if self.valid_user(user_id):
                    return int(user_id)
                print("\n❌ Invalid User ID! Please try again")
                
            elif choice == '2':
                return self.register_user()
                
            elif choice == '3':
                return None
                
            else:
                print("Invalid choice!")

    def valid_user(self, user_id):
        try:
            result = self.conn.execute("SELECT 1 FROM LibraryUsers WHERE UserID = ?", 
                                     (user_id,)).fetchone()
            return bool(result)
        except sqlite3.Error:
            return False

    # User Management
    def register_user(self):
        self.clear_screen()
        print("🐻 New User Registration 🐻")
        while True:
            name = input("Enter your full name: ").strip()
            email = input("Enter email address: ").strip()
            phone = input("Enter phone number: ").strip()
            
            if not all([name, email, phone]):
                print("All fields are required!")
                continue
                
            try:
                self.conn.execute("""
                    INSERT INTO LibraryUsers (Name, Email, Phone)
                    VALUES (?, ?, ?)
                """, (name, email, phone))
                self.conn.commit()
                new_id = self.conn.execute("SELECT last_insert_rowid()").fetchone()[0]
                print(f"\n🎉 Welcome {name}! Your User ID is: {new_id}")
                return new_id
            except sqlite3.IntegrityError:
                print("❌ Error: Email already exists!")
            except sqlite3.Error as e:
                print(f"Database error: {str(e)}")
                return None

    # Borrow/Return Features
    def borrow_item(self):
        user_id = self.get_user_id()
        if not user_id:
            return
            
        self.clear_screen()
        print("📖 Borrow an Item 📖")
        self.search_items()
        
        try:
            item_id = int(input("\nEnter ID of item to borrow: "))
            self.conn.execute("""
                INSERT INTO Borrowing (UserID, ItemID, DueDate)
                VALUES (?, ?, DATE('now', '+14 days'))
            """, (user_id, item_id))
            self.conn.commit()
            print("\n✅ Borrowed successfully! Due in 14 days")
        except ValueError:
            print("Invalid item ID!")
        except sqlite3.Error as e:
            print(f"\n❌ Error: {str(e)}")
        finally:
            self.press_enter()

    #return item
    def return_item(self):
        user_id = self.get_user_id()
        if not user_id:
            return
            
        self.clear_screen()
        print("📗 Return Items 📗")
        try:
            loans = self.conn.execute("""
                SELECT b.TransactionID, i.Title, b.DueDate 
                FROM Borrowing b
                JOIN LibraryItems i ON b.ItemID = i.ItemID
                WHERE b.UserID = ? AND b.ReturnDate IS NULL
            """, (user_id,)).fetchall()
            
            if not loans:
                print("No items to return!")
                self.press_enter()
                return
                
            print("\nYour Current Loans:")
            for loan in loans:
                print(f"{loan['TransactionID']}: {loan['Title']} (Due: {loan['DueDate']})")
            
            trans_id = input("\nEnter transaction ID to return: ")
            self.conn.execute("""
                UPDATE Borrowing SET ReturnDate = DATE('now') 
                WHERE TransactionID = ?
            """, (trans_id,))
            self.conn.commit()
            print("Item returned successfully!")
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        finally:
            self.press_enter()

    # Event Features
    def show_events(self):
        self.clear_screen()
        print("📅 Upcoming Events 📅")
        try:
            events = self.conn.execute("""
                SELECT * FROM Events 
                WHERE EventDate >= DATE('now') 
                ORDER BY EventDate
            """).fetchall()
            
            if not events:
                print("No upcoming events!")
                return
                
            for event in events:
                print(f"""
                ID: {event['EventID']}
                Event: {event['EventName']}
                Date: {event['EventDate']}
                Type: {event['EventType']}
                For: {event['Audience']}
                Room: {event['RoomID']}
                """)
        except sqlite3.Error as e:
            print(f"Database error: {str(e)}")

    # Donate Item
    def donate_item(self):
        self.clear_screen()
        print("🎁 Donate an Item 🎁")
        try:
            title = input("Enter item title: ").strip()
            author = input("Enter author (leave blank if none): ").strip() or None
            item_type = self._get_valid_input(
            "Item type (exact: printBooks/onlineBooks/magazines/scientificJournals/cds/records/other): ",
            ['printBooks','onlineBooks','magazines','scientificJournals','cds','records','other']
            )
            copies = int(input("Number of copies donated: "))
            
            self.conn.execute("""
                INSERT INTO LibraryItems (Title, Author, ItemType, AvailableCopies)
                VALUES (?, ?, ?, ?)
            """, (title, author, item_type, copies))
            self.conn.commit()
            print("\n✅ Thank you for your donation!")
        except ValueError:
            print("Invalid number of copies!")
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        self.press_enter()

    # Register for events
    def register_for_event(self):
        user_id = self.get_user_id()
        if not user_id:
            return
        
        self.clear_screen()
        print("🎟️ Register for Event 🎟️")
        events = self.conn.execute("""
            SELECT * FROM Events 
            WHERE EventDate >= DATE('now')
            ORDER BY EventDate
        """).fetchall()
        
        if not events:
            print("No upcoming events!")
            self.press_enter()
            return
        
        for event in events:
            print(f"{event['EventID']}: {event['EventName']} ({event['EventDate']})")
        
        try:
            event_id = int(input("\nEnter Event ID: "))
            self.conn.execute("""
                INSERT INTO EventRegistrations (UserID, EventID)
                VALUES (?, ?)
            """, (user_id, event_id))
            self.conn.commit()
            print("Registration successful!")
        except sqlite3.IntegrityError:
            print("You're already registered for this event!")
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        self.press_enter()


    # Volunteer
    def volunteer(self):
        user_id = self.get_user_id()
        if not user_id:
            return
        
        self.clear_screen()
        print("🤝 Volunteer Registration 🤝")
        role = self._get_valid_input(
            "Role (General/Event Helper/Book Sorting/Other): ",
            ['General', 'Event Helper', 'Book Sorting', 'Other']
        )
        start_date = input("Start date (YYYY-MM-DD): ")
        
        try:
            self.conn.execute("""
                INSERT INTO Volunteers (UserID, Role, StartDate)
                VALUES (?, ?, ?)
            """, (user_id, role, start_date))
            self.conn.commit()
            print("Thank you for volunteering!")
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        self.press_enter()

    # Ask for help
    def ask_for_help(self):
        user_id = self.get_user_id()
        if not user_id:
            return
        
        self.clear_screen()
        print("🆘 Ask for Help 🆘")
        librarians = self.conn.execute("""
            SELECT StaffID, Name FROM LibraryPersonnel
            WHERE Position = 'Librarian'
        """).fetchall()
        
        if not librarians:
            print("No librarians available!")
            self.press_enter()
            return
        
        print("Available Librarians:")
        for lib in librarians:
            print(f"{lib['StaffID']}: {lib['Name']}")
        
        try:
            staff_id = int(input("\nEnter Librarian ID: "))
            request = input("Describe your request: ")
            self.conn.execute("""
                INSERT INTO HelpRequests (UserID, StaffID, RequestText)
                VALUES (?, ?, ?)
            """, (user_id, staff_id, request))
            self.conn.commit()
            print("Help request submitted!")
        except sqlite3.Error as e:
            print(f"Error: {str(e)}")
        self.press_enter()


    # Delete Account
    def delete_account(self):
        self.clear_screen()
        print("🚫 Delete Account 🚫")
        user_id = self.get_user_id()
        if not user_id:
            return
            
        confirm = input("Are you sure? This cannot be undone! (y/n): ").lower()
        if confirm == 'y':
            try:
                self.conn.execute("DELETE FROM LibraryUsers WHERE UserID = ?", (user_id,))
                self.conn.commit()
                print("Account deleted successfully")
            except sqlite3.Error as e:
                print(f"Error deleting account: {str(e)}")
        else:
            print("Account deletion canceled")
        self.press_enter()

    # Main Menu
    def main_menu(self):
        while True:
            self.clear_screen()
            print("""
        🏫 WELCOME TO SMART LIBRARY 🏫
        1. Search Items     7. Volunteer
        2. Borrow Item      8. Ask for Help
        3. Return Item      9. New User
        4. View Events      10. Delete Account
        5. Donate Item      11. Exit
        6. Register Event
        """)
            
            choice = input("Choose (1-11): ")
            
            if choice == '1':
                self.search_items()
                self.press_enter()
            elif choice == '2':
                self.borrow_item()
            elif choice == '3':
                self.return_item()
            elif choice == '4':
                self.show_events()
                self.press_enter()
            elif choice == '5': 
                self.donate_item()
            elif choice == '6': 
                self.register_for_event()
            elif choice == '7': 
                self.volunteer()
            elif choice == '8': 
                self.ask_for_help()
            elif choice == '9':
                self.register_user()
                self.press_enter()
            elif choice == '10':
                self.delete_account()
            elif choice == '11':
                print("Goodbye! 👋")
                sys.exit()
            else:
                print("Invalid choice!")
                self.press_enter()

if __name__ == "__main__":
    LibrarySystem().main_menu()