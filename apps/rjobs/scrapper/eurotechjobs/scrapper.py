import re
import time
import requests
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeEuroTechJobs(IScrapper):
    """
    Scrapper for: https://eurotechjobs.com

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://www.eurotechjobs.com/job_search/category/developer/category/front_end_developer/category/python_developer/category/web_developer",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            """
            <a href="/job_display/253366/Audio_Software_Manager_Jabra_Ballerup">Audio Software Manager</a>
            https://www.eurotechjobs.com/job_display/253366/Audio_Software_Manager_Jabra_Ballerup
            """
            href_matches = re.findall(r'<a href="/job_display/(.*?)">', response.text)
            href_matches = [
                f"https://www.eurotechjobs.com/job_display/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <div class="jobDisplay">
        <!-- Job Description start -->
        <h2 style="text-align: center;">Audio Software Manager</h2>
        """
        h1_pattern = re.compile(
            r'<div class="jobDisplay">.*<h2 style="text-align: center;">(.*)</h2>',
            re.DOTALL,
        )
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="jobDisplay">JD</div>
        """
        pattern = re.compile(
            r'<div class="jobDisplay">(.*)<\/div>',
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
