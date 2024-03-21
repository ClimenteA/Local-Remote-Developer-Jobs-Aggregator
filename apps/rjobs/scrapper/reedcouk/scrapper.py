import re
import time
import requests
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeReedCoUK(IScrapper):
    """
    Scrapper for: https://reed.co.uk

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&dateCreatedOffSet=today",
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&pageno=2&dateCreatedOffSet=today",
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&dateCreatedOffSet=lastthreedays",
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&pageno=2&dateCreatedOffSet=lastthreedays",
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&pageno=3&dateCreatedOffSet=lastthreedays",
            "https://www.reed.co.uk/jobs/work-from-home-it-jobs?keywords=it&parentSectorIds=52&pageno=4&dateCreatedOffSet=lastthreedays",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            """
            <h2 class="job-card_jobResultHeading__title__IQ8iT"><a href="/jobs/project-manager/52355254?source=searchResults&amp;filter=%2Fjobs%2Fwork-from-home-it-jobs%3Fkeywords%3Dit%26parentSectorIds%3D52%26dateCreatedOffSet%3Dtoday" class="" data-id="52355254" title="Project Manager" data-qa="job-card-title" data-gtm="job_click" data-gtm-value="52355254" data-page-component="job_card" data-element="job_title">Project Manager</a></h2>
            https://www.reed.co.uk/jobs/project-manager/52355254?source=searchResults&filter=%2Fjobs%2Fwork-from-home-it-jobs%3Fkeywords%3Dit%26parentSectorIds%3D52%26dateCreatedOffSet%3Dtoday
            """
            href_matches = re.findall(
                r'<h2 class="job-card_jobResultHeading__title__IQ8iT"><a.*data-id="{.*?}">',
                response.text,
            )
            href_matches = [
                f"https://www.reed.co.uk/jobs/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1 class="job-title">
            Senior Big Data Engineer
        </h1>
        """
        h1_pattern = re.compile(r'<h1 class="job-title">(.*?)<\/h1>', re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="description">JD</div>
        """
        pattern = re.compile(
            r'<div class="description">(.*?)<\/div>',
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
