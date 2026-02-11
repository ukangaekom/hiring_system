from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel

class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    requirements: str
    department: Optional[str] = None
    date_posted: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="Open")
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    organization_id: int = Field(foreign_key="organization.id")
    
    organization: "Organization" = Relationship(back_populates="jobs")
    applications: List["Application"] = Relationship(back_populates="job")
