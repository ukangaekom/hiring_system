from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime

class Application(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    job_id: int = Field(foreign_key="job.id")
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pending") # pending, accepted, rejected
    
    user: "User" = Relationship(back_populates="applications")
    job: "Job" = Relationship(back_populates="applications")
