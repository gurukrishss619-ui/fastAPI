
from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str