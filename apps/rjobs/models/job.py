from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel


class Job(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    url: str
    applied: Optional[bool] = Field(default=False)
    ignored: Optional[bool] = Field(default=False)
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
