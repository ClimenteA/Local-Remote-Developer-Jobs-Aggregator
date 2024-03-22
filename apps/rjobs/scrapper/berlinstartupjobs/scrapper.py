import re
import time
import requests
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeBerlinStartupJobs(IScrapper):
    """
    Scrapper for: berlinstartupjobs.com

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://berlinstartupjobs.com/skill-areas/javascript/",
            "https://berlinstartupjobs.com/skill-areas/python/",
            "https://berlinstartupjobs.com/skill-areas/typescript/",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            """
            <a href="https://berlinstartupjobs.com/engineering/senior-developer-fullstack-typescript-javascript-node-js-m-f-d-datatroniq/">(Senior) Developer Fullstack (Typescript / Javascript / Node.js)</a>
            https://berlinstartupjobs.com/engineering/senior-developer-fullstack-typescript-javascript-node-js-m-f-d-datatroniq/
            """
            href_matches = re.findall(
                r'<a href="https://berlinstartupjobs.com/engineering/(.*?)">',
                response.text,
            )
            href_matches = [
                f"https://berlinstartupjobs.com/engineering/{partial_url}"
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
        <div class="bsj-template__content">JD</div>
        """
        pattern = re.compile(
            r'<div class="bsj-template__content">(.*)</div>',
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
