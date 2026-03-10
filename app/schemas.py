
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(User):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)