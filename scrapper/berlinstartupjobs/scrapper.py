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
        urls = [
            "https://berlinstartupjobs.com/skill-areas/javascript/",
            "https://berlinstartupjobs.com/skill-areas/python/",
            "https://berlinstartupjobs.com/skill-areas/typescript/",
        ]

        job_description_urls = []
        for url in urls:
            log.info(f"Getting urls to JD from: {url}")
            response = requests.get(url, headers=self.headers)
            """
            <a href="https://berlinstartupjobs.com/engineering/senior-developer-fullstack-typescript-javascript-node-js-m-f-d-datatroniq/">(Senior) Developer Fullstack (Typescript / Javascript / Node.js)</a>
            https://berlinstartupjobs.com/engineering/senior-developer-fullstack-typescript-javascript-node-js-m-f-d-datatroniq/
            """

            raise Exception(response.text)

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
            log.info("Done!")

        log.success(f"Finished getting urls for JD Urls: {job_description_urls}")
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

            jobs = []
            for job_url in job_description_urls:
                log.info("Getting JD from url: ", job_url)
                response = requests.get(job_url, headers=self.headers)
                job = Job(
                    title=self.get_job_title(response.text),
                    description=self.get_job_description(response.text),
                    url=job_url,
                )
                jobs.append(job)
                time.sleep(0.5)  # trying not to get blocked
                log.info("Done!")

            log.success("Finished getting JD!")
            return [job.as_dict() for job in jobs]

        except Exception as err:
            log.exception(err)
            return None
