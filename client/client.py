import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

def get_all_books():
    response = requests.get (f"{BASE_URL}/books")
    print_response (response)

def get_book (book_id):
    response = requests.get (f"{BASE_URL}/books/{book_id}")
    print_response (response)

def create_book (title, author_name, author_email, year, genre) :
    book = {
        "id": len(requests.get (f"{BASE_URL}/books").json()) + 1,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre
    }

    response = requests.post (f"{BASE_URL}/books", json=book)
    print_response (response)

def update_book (book_id, title, author_name, author_email, year, genre):
    book = {
        "id": book_id,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre
    }

    response = requests.put (f"{BASE_URL}/books/{book_id}", json=book)
    print_response (response)

def delete_book (book_id) :
    response = requests.delete (f"{BASE_URL}/books/{book_id}")
    print_response (response)

def print_response (response) :
    try:

        print(f"Status Code: {response.status_code}")
        print(json.dumps (response.json(), indent=2))
    except ValueError:
        print(f"Status Code: {response.status_code}")
        print (response.text)

def main():
    parser = argparse.ArgumentParser (description="Book API Client")
    subparsers = parser.add_subparsers (dest="command", help="API command")

# List all books
    subparsers.add_parser("list", help="List all books")

# Get a book
    get_parser = subparsers.add_parser("get", help="Get a book by ID")
    get_parser.add_argument ("id", type=int, help="Book ID")

# Create a book
    create_parser = subparsers.add_parser("create", help="Create a new book")
    create_parser.add_argument ("title", type=str, help="Book title")
    create_parser.add_argument ("author_name", type=str, help="Author name")
    create_parser.add_argument ("--author_email", type=str, default=None,
                                help="Author email")
    create_parser.add_argument ("year", type=int, help="Publication year")
    create_parser.add_argument ("genre", type=str, help="Book genre")

# Update a book
    update_parser = subparsers.add_parser ("update", help="Update a book")
    update_parser.add_argument ("id", type=int, help="Book ID")
    update_parser.add_argument ("title", type=str, help="Book title")
    update_parser.add_argument ("author_name", type=str, help="Author name")
    update_parser.add_argument ("--author_email", type=str, default=None,
                                help="Author email")
    update_parser.add_argument ("year", type=int, help="Publication year")
    update_parser.add_argument ("genre", type=str, help="Book genre")

# Delete a book
    delete_parser = subparsers.add_parser ("delete", help="Delete a book")
    delete_parser.add_argument ("id", type=int, help="Book ID")

    args = parser.parse_args ()

    if args.command == "list":
        get_all_books ()
    elif args.command == "get":
        get_book (args.id)
    elif args.command == "create":
        create_book (args.title, args.author_name, args.author_email, args.year,
                     args.genre)
    elif args.command == "update":
        update_book (args.id, args.title, args.author_name, args.author_email,
                     args.year, args.genre)
    elif args.command == "delete":
        delete_book (args.id)
    else:
        parser.print_help ()

if __name__ == "__main__":
    main()