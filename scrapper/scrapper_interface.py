import abc
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


class IScrapper(abc.ABC):
    @abc.abstractmethod
    def scrape(self): ...


@dataclass
class Job:
    title: str
    description: str
    url: str
    applied: Optional[bool] = field(default=False)
    ignored: Optional[bool] = field(default=False)
    timestamp: Optional[str] = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        assert isinstance(self.title, str), "Title must be string!"
        assert isinstance(self.description, str), "Description must be string!"
        assert isinstance(self.url, str), "Url must be string!"
        assert isinstance(self.applied, bool), "Applied must be boolean!"
        assert isinstance(self.ignored, bool), "Ignored must be boolean!"
        assert isinstance(self.timestamp, str), "Timestamp must be string!"
