from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    jobs: List["Job"] = Relationship(back_populates="organization")
