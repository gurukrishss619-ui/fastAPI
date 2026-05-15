from fastapi import FastAPI
from fastapi import exceptions, HTTPException, status
from methods.BookClasses import Book, BookUpdate
from databases.NoSQL import books

app = FastAPI()


@app.get("/book")
def get_books():
    return books


@app.get("/book/{id}")
def get_book_id(book_id: int):
    for book in books:
        if book['id'] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 

@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return "Book successfully created"


@app.put("/book/{id}")
def edit_book(book_id: int, book_update: BookUpdate):
    for book in books:
        if book['id'] == book_id:
            book['name'] = book_update.name
            return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 


@app.delete("/book/{id}")
def delete_book(book_id: int):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return {"message":"Book successfully removed"}
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")