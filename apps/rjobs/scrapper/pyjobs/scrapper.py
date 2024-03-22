import re
import time
import requests
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapePyJobs(IScrapper):
    """
    Scrapper for: https://pyjobs.com

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://www.pyjobs.com/?remoteLevel[0]=1&remoteLevel[1]=2&date=72&regions[0]=RO",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            """
            <a href="https://www.pyjobs.com/job/senior-pythonelasticsearch-developer-oMyKNnGy" class="">
                            <span class="absolute -inset-x-4 inset-y-[calc(-1*(theme(spacing.6)+1px))] md:-inset-x-6 md:rounded-2xl lg:-inset-x-8 z-10"></span>
                            <span>Senior Python/Elasticsearch Developer</span>
                        </a>
            """
            href_matches = re.findall(
                r'<a href="https://www.pyjobs.com/job/(.*?)" class="">',
                response.text,
            )
            href_matches = [
                f"https://www.pyjobs.com/job/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1>
            PHP Laravel Developer
        </h1>
        """
        h1_pattern = re.compile(r"<h1>(.*?)<\/h1>", re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="prose">JD</div>
        """
        pattern = re.compile(
            r'<div class="prose">(.*)</div>',
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
