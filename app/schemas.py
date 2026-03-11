
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Post(BaseModel):
    title:str
    slug:str
    content:str
    published:bool

class PostResponse(Post):
    id:int
    created_at:datetime
    owner:UserResponse