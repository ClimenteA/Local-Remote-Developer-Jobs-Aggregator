import re
import time
import requests
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeReactJobs(IScrapper):
    """
    Scrapper for: https://reactjobs.io
    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        url = "https://reactjobs.io/jobs/javascript?search=Javascript&isRemote=true"

        job_description_urls = []
        for page in range(4):
            page = str(page + 1)
            response = requests.get(url, headers=headers)
            href_matches = re.findall(
                r'<a href="https://reactjobs.io/react-jobs/{.*?}"', response.text
            )
            href_matches = [
                f"https://reactjobs.io/react-jobs/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl ">
            React + React Native Developer
        </h1>
        """
        h1_pattern = re.compile(
            r'<h1 class="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl[^>]*>(.*?)<\/h1>',
            re.DOTALL,
        )
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="prose prose-sm prose-slate max-w-none">JD</div>
        """
        pattern = re.compile(
            r'<div class="prose prose-sm prose-slate max-w-none">(.*?)<\/div>',
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
