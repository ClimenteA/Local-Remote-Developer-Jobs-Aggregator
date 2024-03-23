import re
import time
import requests
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeWeWorkRemotely(IScrapper):
    """
    Scrapper for: https://weworkremotely.com/

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://weworkremotely.com/categories/remote-full-stack-programming-jobs",
            "https://weworkremotely.com/categories/remote-front-end-programming-jobs",
            "https://weworkremotely.com/categories/remote-back-end-programming-jobs",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            href_matches = re.findall(r'<a href="/remote-jobs/(.*?)">', response.text)
            href_matches = [
                f"https://weworkremotely.com/remote-jobs/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1>
            Senior Machine Learning Engineer
        </h1>
        """
        h1_pattern = re.compile(r"<h1>(.*?)<\/h1>", re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="listing-container" id="job-listing-show-container">JD</div>
        """
        pattern = re.compile(
            r'<div class="listing-container" id="job-listing-show-container">(.*?)<\/div>',
            re.DOTALL,
        )
        match = pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def scrape(self):
        try:
            job_description_urls = self.get_job_description_urls()

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            }

            jobs = []
            for job_url in job_description_urls:
                response = requests.get(job_url, headers=headers)
                job = Job(
                    title=self.get_job_title(response.text),
                    description=self.get_job_description(response.text),
                    url=job_url,
                )
                jobs.append(job)
                time.sleep(0.5)  # trying not to get blocked

            return jobs

        except Exception as err:
            log.exception(err)
            return None
