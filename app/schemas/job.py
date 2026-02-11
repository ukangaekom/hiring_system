from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

class JobBase(BaseModel):
    title: str
    description: str
    requirements: str
    department: Optional[str] = None
    status: str = "Open"
    min_age: Optional[int] = None
    max_age: Optional[int] = None

class JobCreate(JobBase):
    pass

class JobRead(JobBase):
    id: int
    organization_id: int
    date_posted: datetime

class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
