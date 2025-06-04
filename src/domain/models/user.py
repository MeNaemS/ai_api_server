from typing import Optional
from pydantic import BaseModel


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
