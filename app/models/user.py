from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
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
    date_registered: datetime = Field(default_factory=datetime.utcnow)
    is_verified: bool = Field(default=False)
    cv_path: Optional[str] = Field(default=None)
    
    applications: List["Application"] = Relationship(back_populates="user")
