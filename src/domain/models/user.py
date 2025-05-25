from typing import Optional
from pydantic import BaseModel


class UserInDB(BaseModel):
    id: int
    login: str
    email: Optional[str]
    full_name: Optional[int]
    password: str
    input_tokens: Optional[int]
    output_tokens: Optional[int]


class AuthUser(BaseModel):
    login: str
    password: str


class FullName(BaseModel):
    name: str
    surname: str
    patronymic: Optional[str] = None


class RegisterUser(BaseModel):
    login: str
    email: Optional[str] = None
    full_name: Optional[FullName] = None
    password: str
