import re
import time
import requests
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeEuRemoteJobs(IScrapper):
    """
    Scrapper for: https://euremotejobs.com

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        data = {
            "lang": "",
            "search_categories[]": "engineering",
            "search_keywords": "",
            "search_location": "",
            "per_page": "12",
            "orderby": "featured",
            "order": "DESC",
            "show_pagination": "false",
        }

        url = "https://euremotejobs.com/jm-ajax/get_listings/"

        # Get links to job description
        job_description_urls = []
        for page in range(2):
            data["page"] = str(page + 1)
            response = requests.post(url, headers=headers, data=data)
            data = response.json()
            data_href_matches = re.findall(r'data-href="(.*?)"', data["showing_links"])
            job_description_urls.extend(data_href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1 class="page-title">
            Senior Machine Learning Engineer
        </h1>
        """
        h1_pattern = re.compile(r'<h1 class="page-title"[^>]*>(.*?)<\/h1>', re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <h2 class="widget-title widget-title--job_listing-top job-overview-title">Overview</h2>
        job description here
        <p class="job_tags">
        """
        pattern = re.compile(
            r'<h2 class="widget-title widget-title--job_listing-top job-overview-title">Overview<\/h2>(.*?)<p class="job_tags">',
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
