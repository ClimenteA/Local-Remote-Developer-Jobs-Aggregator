import abc
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


class IScrapper(abc.ABC):
    headers = {
        "accept": "*/*",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
    }

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
        assert len(self.title) > 0, "Title empty!"
        assert len(self.description) > 0, "Description empty!"
        assert len(self.url) > 0, "Url empty!"
        assert isinstance(self.applied, bool), "Applied must be boolean!"
        assert isinstance(self.ignored, bool), "Ignored must be boolean!"
        assert isinstance(self.timestamp, str), "Timestamp must be string!"

    def as_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "applied": self.applied,
            "ignored": self.ignored,
            "timestamp": self.timestamp,
        }
