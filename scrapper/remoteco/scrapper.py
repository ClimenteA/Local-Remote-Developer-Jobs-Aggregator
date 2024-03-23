import re
import requests
import time
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeRemoteCo(IScrapper):
    """
    Scrapper for: https://remote.co
    """

    def get_job_description_urls(self, page: int = 1):
        url = f"https://remote.co/remote-jobs/developer/page/{page}/"
        response = requests.get(url)

        job_description_urls = re.findall(r'<a href="\/job\/(.*?)"', response.text)
        job_description_urls = [
            f"https://remote.co/job/{href}" for href in job_description_urls
        ]

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1 class="font-weight-bold">
            Senior Fullstack Software Engineer – Core Experiences at CaptivateIQ
        </h1>
        """
        h1_pattern = re.compile(r'<h1 class="font-weight-bold">(.*?)<\/h1>', re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="single_job_listing">JD</div>
        """
        pattern = re.compile(r'<div class="single_job_listing">(.*?)<\/div>', re.DOTALL)
        match = pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def scrape(self):
        try:
            batch1 = self.get_job_description_urls(1)
            batch2 = self.get_job_description_urls(2)
            jd_urls = batch1 + batch2

            jobs = []
            for jdurl in jd_urls:
                response = requests.get(jdurl)
                job = Job(
                    title=self.get_job_title(response.text),
                    description=self.get_job_description(response.text),
                    url=jdurl,
                )
                jobs.append(job)
                time.sleep(0.5)  # trying not to get blocked

            return jobs

        except Exception as err:
            log.exception(err)
            return None
