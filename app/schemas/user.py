from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    qualification: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    age: Optional[int] = None
    desired_job: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    is_verified: bool
    cv_path: Optional[str] = None
    date_registered: datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str
