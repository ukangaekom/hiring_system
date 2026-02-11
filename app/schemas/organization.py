from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr

class OrganizationBase(BaseModel):
    email: EmailStr
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    password: str

class OrganizationRead(OrganizationBase):
    id: int
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    created_at: datetime

class OrganizationLogin(BaseModel):
    email: EmailStr
    password: str
