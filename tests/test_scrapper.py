import unittest
import json
from scrapper.berlinstartupjobs.scrapper import ScrapeBerlinStartupJobs


# python -m unittest tests.test_scrapper.TestScrapper
# python -m unittest tests.test_scrapper.TestScrapper.test_berlin_startup_jobs


class TestScrapper(unittest.TestCase):
    def test_berlin_startup_jobs(self):
        scrapper = ScrapeBerlinStartupJobs()
        data = scrapper.scrape()

        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

        with open("jobs.json", "w") as f:
            f.write(json.dumps(data))
