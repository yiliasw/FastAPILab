from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
import uvicorn

app = FastAPI()

# Define complex object models
class Author (BaseModel) :
    name: str
    email: Optional [str] = None

class Book (BaseModel) :
    id: int
    title: str
    author: Author
    year: int
    genre: str
    rating: Optional[List[int]] = Field (default=None, description="Rating must be between 1 and 5")

# In-memory dataset
books = [
    Book (
        id=1,
        title="The Great Gatsby",
        author=Author (name="F. Scott Fitzgerald", email="fscott@example.com"),
        year=1925,
        genre="Fiction"
    ),
    Book (
        id=2,
        title="1984",
        author=Author (name="George Orwell"),
        year=1949,
        genre="Dystopian"
    ),
    Book(
        id=3,
        title="To Kill a Mockingbird",
        author=Author (name="Harper Lee"),
        year=1960,
        genre="Fiction",
        rating=[5, 4, 5]
    )
]

# GET all books
@app.get ("/books", response_model=List [Book])
async def get_all_books ():
    return books
# get book count
@app.get("/books/count")
async def get_book_count():
    return {"count": len(books)}
# GET books by genre
@app.get ("/books/genre/{genre}", response_model=List [Book])
async def get_books_by_genre (genre: str):
    books_by_genre = []
    for book in books:
        if book.genre == genre:
            books_by_genre.append(book)
    if not books_by_genre:
        raise HTTPException (status_code=404, detail="No books found for the specified genre")
    return books_by_genre
 
# GET a book by ID
@app.get ("/books/{book_id}", response_model=Book)
async def get_book (book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException (status_code=404, detail="Book not found")

# POST a new book
@app.post ("/books", response_model=Book)
async def create_book(book: Book) :
    if any(b.id == book.id for b in books) :
        raise HTTPException (status_code=400, detail="Book ID already exists")
    books.append (book)
    return book

# PUT to update a book
@app.put ("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book) :
    for i, book in enumerate (books) :
        if book.id == book_id:
            books [i] = updated_book
            return updated_book
    raise HTTPException (status_code=404, detail="Book not found")

# partial update of a book
@app.patch("/books/{book_id}", response_model=Book)
async def partial_update_book(book_id: int, updated_fields: dict):
    for index, book in enumerate(books):
        if book.id == book_id:
            book_data = book.model_dump()
            book_data.update(updated_fields)
            books[index] = Book(**book_data)
            return books[index]

    raise HTTPException(status_code=404, detail="Book not found")
# DELETE a book
@app.delete ("/books/{book_id}")
async def delete_book(book_id: int):
    for i, book in enumerate (books) :
        if book.id == book_id:
            books.pop(i)
            return {"message": "Book deleted"}
    raise HTTPException (status_code=404, detail="Book not found")


if __name__ == "__main__":
    uvicorn.run(app, host ="0.0.0.0", port=8000)