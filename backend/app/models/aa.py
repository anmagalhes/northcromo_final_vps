# app/models/aa.py
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):  # ou User(Base) se usando SQLAlchemy puro
    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str