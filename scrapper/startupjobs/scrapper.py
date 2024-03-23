import time
import requests
import datetime
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeStartupJobs(IScrapper):
    """
    Scrapper for: startup.jobs


    """

    def scrape(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
            }
            url = "https://startup.jobs/?remote=true"

            response = requests.get(url, headers=headers)
            rawjsonlist = [d for d in response.json() if d["isFullRemote"]]

            # TODO not sure how to handle requests graphql..
            jobs = []
            for d in rawjsonlist:
                job_url = f"https://devjob.ro/api/jobWithUrl/{d['jobUrl']}"

                response = requests.get(job_url, headers=headers)
                details = response.json()

                job = Job(
                    title=d["name"],
                    description=f"""
                    <div>
                    <p>Company: {d["company"]}</p>
                    <p>{details["description"]}</p>
                    <p>{details["requirementsMustTextArea"]}</p>
                    <p>{details["requirementsNiceTextArea"]}</p>
                    <p>{details["responsibilitiesTextArea"]}</p>                    
                    <p>Tech: {d["techCategory"]}, {", ".join(d["technologies"])}</p>
                    <p>Location: {d["cityCategory"]}</p>
                    </div>
                    """,
                    url=job_url,
                    timestamp=datetime.datetime.fromisoformat(
                        d["createdAt"]
                    ).isoformat(),
                )

                jobs.append(job)
                time.sleep(0.5)  # trying not to get blocked

            return jobs

        except Exception as err:
            log.exception(err)
            return None
