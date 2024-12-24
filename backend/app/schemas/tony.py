from pydantic import BaseModel, EmailStr, Field, validator

class Message (BaseModel):
    Message: str

class UserSchema (BaseModel):
    username: str
    email: EmailStr
    password: str

