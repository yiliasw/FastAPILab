import argparse
import json
import requests

BASE_URL = "http://localhost:8000"

def parse_ratings(value):
    """Parse a comma-separated list of ratings, each from 1 through 5."""
    try:
        ratings = [int(item.strip()) for item in value.split(",")]
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "ratings must be comma-separated integers"
        ) from exc

    if not ratings or any(rating not in range(1, 6) for rating in ratings):
        raise argparse.ArgumentTypeError(
            "each rating must be an integer from 1 to 5"
        )

    return ratings

def get_all_books():
    response = requests.get (f"{BASE_URL}/books")
    print_response (response)

def get_book_count():
    response = requests.get (f"{BASE_URL}/books/count")
    print_response (response)

def get_books_by_genre (genre:str):
    response = requests.get (f"{BASE_URL}/books/genre/{genre}")
    print_response (response)

def get_book (book_id:int):
    response = requests.get (f"{BASE_URL}/books/{book_id}")
    print_response (response)

def create_book (title, author_name, author_email, year, genre, rating):
    book = {
        "id": len(requests.get (f"{BASE_URL}/books").json()) + 1,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "rating": rating
    }

    response = requests.post (f"{BASE_URL}/books", json=book)
    print_response (response)

def update_book (book_id, title, author_name, author_email, year, genre, rating):
    book = {
        "id": book_id,
        "title": title,
        "author": {"name": author_name, "email": author_email},
        "year": year,
        "genre": genre,
        "rating": rating
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
def patch_book (book_id, title=None, year=None, genre=None, rating=None):
    updated_fields = {}
    if title is not None:
        updated_fields["title"] = title
    if year is not None:
        updated_fields["year"] = year
    if genre is not None:
        updated_fields["genre"] = genre
    if rating is not None:
        updated_fields["rating"] = rating

    response = requests.patch (
        f"{BASE_URL}/books/{book_id}", json=updated_fields
    )
    print_response (response)

def main():
    parser = argparse.ArgumentParser (description="Book API Client")
    subparsers = parser.add_subparsers (dest="command", help="API command")

# List all books
    subparsers.add_parser("list", help="List all books")

# Get book count
    subparsers.add_parser("count", help="Get the total count of books")

# Get a book
    get_parser = subparsers.add_parser("get", help="Get a book by ID")
    get_parser.add_argument ("id", type=int, help="Book ID")
    genre_parser = subparsers.add_parser("genre",help="Find books by genre",)
    genre_parser.add_argument("genre", type=str, help="Book genre")
# Create a book
    create_parser = subparsers.add_parser("create", help="Create a new book")
    create_parser.add_argument ("title", type=str, help="Book title")
    create_parser.add_argument ("author_name", type=str, help="Author name")
    create_parser.add_argument ("--author_email", type=str, default=None,
                                help="Author email")
    create_parser.add_argument ("year", type=int, help="Publication year")
    create_parser.add_argument ("genre", type=str, help="Book genre")
    create_parser.add_argument ("rating", type=parse_ratings,
                                help="Comma-separated ratings (each 1-5)")
# Update a book
    update_parser = subparsers.add_parser ("update", help="Update a book")
    update_parser.add_argument ("id", type=int, help="Book ID")
    update_parser.add_argument ("title", type=str, help="Book title")
    update_parser.add_argument ("author_name", type=str, help="Author name")
    update_parser.add_argument ("--author_email", type=str, default=None,
                                help="Author email")
    update_parser.add_argument ("year", type=int, help="Publication year")
    update_parser.add_argument ("genre", type=str, help="Book genre")
    update_parser.add_argument ("rating", type=parse_ratings,
                                help="Comma-separated ratings (each 1-5)")
# Partially update a book
    patch_parser = subparsers.add_parser ("patch", help="Partially update a book")
    patch_parser.add_argument ("id", type=int, help="Book ID")
    patch_parser.add_argument ("--title", type=str, help="New book title")
    patch_parser.add_argument ("--year", type=int, help="New publication year")
    patch_parser.add_argument ("--genre", type=str, help="New book genre")
    patch_parser.add_argument (
        "--rating", type=parse_ratings,
        help="New comma-separated ratings (each 1-5)"
    )

# Delete a book
    delete_parser = subparsers.add_parser ("delete", help="Delete a book")
    delete_parser.add_argument ("id", type=int, help="Book ID")

    args = parser.parse_args ()

    if args.command == "list":
        get_all_books ()
    elif args.command == "get":
        get_book (args.id)
    elif args.command == "count":
        get_book_count()
    elif args.command == "genre":
        get_books_by_genre (args.genre)
    elif args.command == "create":
        create_book (args.title, args.author_name, args.author_email, args.year,
                     args.genre, args.rating)
    elif args.command == "update":
        update_book (args.id, args.title, args.author_name, args.author_email,
                     args.year, args.genre, args.rating)
    elif args.command == "patch":
        patch_book (args.id, args.title, args.year, args.genre, args.rating)
    elif args.command == "delete":
        delete_book (args.id)
    else:
        parser.print_help ()

if __name__ == "__main__":
    main()