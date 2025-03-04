import json
import os
from datetime import datetime, timedelta

# File paths and configuration
BOOKS_FILE = "Books.json"
LOG_FILE = "Log file.log"
BORROW_PERIOD = 7  # days allowed for borrowing
FINE_PER_DAY = 1.0  # fine amount per overdue day

def load_books():
    """Load the book records from a JSON file."""
    if not os.path.exists(BOOKS_FILE):
        return []
    with open(BOOKS_FILE, "r") as f:
        return json.load(f)

def save_books(books):
    """Save the current list of books to the JSON file."""
    with open(BOOKS_FILE, "w") as f:
        json.dump(books, f, indent=4)

def log_transaction(message):
    """Append a transaction message with a timestamp to the log file."""
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now().isoformat()} - {message}\n")

def list_books(books):
    """Display all books and their statuses."""
    if not books:
        print("No books available.")
        return
    print("\nAvailable Books:")
    for book in books:
        status = "Available" if book["available"] else f"Borrowed by {book.get('borrower', 'N/A')}"
        print(f"Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, "
              f"Genre: {book.get('genre','N/A')}, Status: {status}")

def search_books(books, query, field):
    """Filter books based on a search query and field."""
    results = [book for book in books if query.lower() in book.get(field, "").lower()]
    return results

def borrow_book(books):
    """Handle borrowing of a book."""
    isbn = input("Enter ISBN of the book to borrow: ").strip()
    for book in books:
        if book["isbn"] == isbn:
            if not book["available"]:
                print("Sorry, this book is currently borrowed.")
                return
            borrower = input("Enter your name: ").strip()
            borrow_date = datetime.now()
            due_date = borrow_date + timedelta(days=BORROW_PERIOD)
            book["available"] = False
            book["borrower"] = borrower
            book["borrow_date"] = borrow_date.isoformat()
            book["due_date"] = due_date.isoformat()
            save_books(books)
            log_transaction(f"{borrower} borrowed '{book['title']}' (ISBN: {isbn}). Due date: {due_date.date()}")
            print(f"You have successfully borrowed '{book['title']}'. It is due on {due_date.date()}.")
            return
    print("Book with given ISBN not found.")

def return_book(books):
    """Handle returning of a book and fine calculation if overdue."""
    isbn = input("Enter ISBN of the book to return: ").strip()
    for book in books:
        if book["isbn"] == isbn:
            if book["available"]:
                print("This book is not currently borrowed.")
                return
            borrower = book.get("borrower", "Unknown")
            due_date_str = book.get("due_date")
            due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
            return_date = datetime.now()
            fine = 0
            if due_date and return_date > due_date:
                overdue_days = (return_date - due_date).days
                fine = overdue_days * FINE_PER_DAY
            # Update book record
            book["available"] = True
            book["borrower"] = ""
            book["borrow_date"] = ""
            book["due_date"] = ""
            save_books(books)
            log_transaction(f"{borrower} returned '{book['title']}' (ISBN: {isbn}). Fine: ${fine:.2f}")
            print(f"Book '{book['title']}' returned successfully.")
            if fine > 0:
                print(f"You have a fine of ${fine:.2f} for overdue return.")
            return
    print("Book with given ISBN not found.")

def main():
    books = load_books()
    # Initialize sample data if no books exist
    if not books:
        books = [
            {"title": "The 3 Mistakes of My Life", "author": "Chetan Bhagat", "isbn": "9788129135513",
             "genre": "Novel", "available": True, "borrower": "", "borrow_date": "", "due_date": ""},
            {"title": "Think and Grow Rich", "author": "Napoleon Hill", "isbn": "9781788441025",
             "genre": "Self-help book", "available": True, "borrower": "", "borrow_date": "", "due_date": ""},
            {"title": "The Discovery of India", "author": "Jawaharlal Nehru", "isbn": "9780195623598",
             "genre": "History & The Past", "available": True, "borrower": "", "borrow_date": "", "due_date": ""},
            {"title": "Kings of the Chessboard", "author": "Paul van der Sterren", "isbn": "9789492510532",
             "genre": "Biography", "available": True, "borrower": "", "borrow_date": "", "due_date": ""},
            {"title": "2 States: The Story of My Marriage", "author": "Chetan Bhagat", "isbn": "9788129115300",
             "genre": " Romance novel", "available": True, "borrower": "", "borrow_date": "", "due_date": ""},
        ]
        save_books(books)

    while True:
        print("\nLibrary Management System")
        print("1. List all books")
        print("2. Search books")
        print("3. Borrow a book")
        print("4. Return a book")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            list_books(books)
        elif choice == "2":
            print("\nSearch by:\n1. Title\n2. Author\n3. Genre")
            search_choice = input("Choose search field (1-3): ").strip()
            if search_choice == "1":
                query = input("Enter title to search: ").strip()
                results = search_books(books, query, "title")
            elif search_choice == "2":
                query = input("Enter author to search: ").strip()
                results = search_books(books, query, "author")
            elif search_choice == "3":
                query = input("Enter genre to search: ").strip()
                results = search_books(books, query, "genre")
            else:
                print("Invalid search option.")
                continue

            if results:
                print("\nSearch Results:")
                for book in results:
                    status = "Available" if book["available"] else f"Borrowed by {book.get('borrower','N/A')}"
                    print(f"Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, "
                          f"Genre: {book.get('genre','N/A')}, Status: {status}")
            else:
                print("No books found matching your query.")
        elif choice == "3":
            borrow_book(books)
        elif choice == "4":
            return_book(books)
        elif choice == "5":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()

