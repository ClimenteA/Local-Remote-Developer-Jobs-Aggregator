import abc


class IScrapper(abc.ABC):
    @abc.abstractmethod
    def scrape(self): ...
