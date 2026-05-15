from turtle import mode
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from databases.database import engine, get_db
from pydantic import BaseModel
import model
from methods.BookClasses import Book


app = FastAPI()


@app.post("/book")
def add_book(book: Book, db: Session=Depends(get_db)):
    new_book = model.BookTable(id=book.id, name=book.name)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"message":"The book has been added", "book":new_book}

@app.get("/book/{book_id}")
def get_book_by_id(book_id: int, db: Session=Depends(get_db)):
    books = db.query(model.BookTable).all()

    for x in range(len(books)):
        if books[x].id == book_id:
            return books[x]

    return books.id

@app.get("/book")
def get_book(db: Session=Depends(get_db)):
    books = db.query(model.BookTable).all()
    return books