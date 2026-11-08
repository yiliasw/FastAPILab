# FastAPILab: bookManagement API
This project is an implementation of a FastAPI server and Python client to mange a book collection using RESTful APIs and JSON serialization.


# setup
1. Create a virtual environment: python -m venv venv'
2. Activate it: 'source venv/bin/activate'
3. Install dependencies: 'pip install -r requirements. txt'

## Running the Server
... bash
cd server
python main.py

## Search books by genre(exercise 1)
to search through terminal:
python client.py genre <genre>

to search through URL:
/books/genre/{genre}

## Add book ratings(exercise 2)
rating is now an attribute of the book object, and is a list of integers greater than or equal to 1 and less than or equal to 5.

## Partial updates with patch(exercise 3)
python client.py patch <id> <--field> <value> to update a book without having to enter every field.



## Book count(exercise 5)
use python client.py count to get a count of all books.








