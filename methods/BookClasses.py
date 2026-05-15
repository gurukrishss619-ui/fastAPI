from pydantic import BaseModel

class Book(BaseModel):
    id: int
    name: str


class BookUpdate(BaseModel):
    name: str







