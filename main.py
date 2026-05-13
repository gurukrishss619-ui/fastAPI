from fastapi import FastAPI
from typing import Optional

app = FastAPI()

@app.get("/")
def main_root():
    return {"message":"Home page"}

@app.get("/greet") 
def greet():
    return {"message":"Hello Guru"}

@app.get("/greet/")
def greet_name(name: str, id: Optional[int] = None):
    return {"message":f"Hello {name} - {id}"}