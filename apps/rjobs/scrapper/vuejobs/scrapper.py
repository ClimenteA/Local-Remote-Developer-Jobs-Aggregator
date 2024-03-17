import requests
import datetime
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeRemotive(IScrapper):
    """

    Scrapper for: https://vuejobs.com/

    Using the api provided that returns:

    {
    "data": [
        {
            "title": "Full Stack Engineer (Java, Vue.js)",
            "slug": "modus-create-full-stack-engineer-java-vue-js",
            "link": "https:\/\/vuejobs.com\/jobs\/modus-create-full-stack-engineer-java-vue-js",
            "description": "Hi there! Modus Create is looking for Full Stack Engineers to join our team. We need professionals with strong experience in Node and Vue.js (vue is a must)We're looking for a Full...",
            "locations": [
                {
                    "name": "Brazil",
                    "city": null,
                    "state": [],
                    "country": {
                        "code": "BR",
                        "name": "Brazil"
                    }
                },
                etc
            ],
            "remote": {
                "type": "ONLY",
                "timezones": [
                    {
                        "tz": "America\/New_York",
                        "offset": 5
                    }
                ]
            },
            "work_permit": null,
            "organization": {
                "name": "Modus Create",
                "avatar": "https:\/\/app.vuejobs.com\/storage\/2122\/da7faef9-13bc-46b9-90a0-ce0ab0b41c0c.com",
                "verified": true
            },
            "salary": {
                "interval": "HOUR",
                "from": 37,
                "to": 40,
                "currency": "USD"
            },
            "taxonomies": {
                "work_type": [
                    "contract"
                ],
                "work_level": [
                    "senior"
                ]
            },
            "published_at": "2024-03-16T18:09:08+01:00",
            "options": {
                "base": true,
                "vuejs-org": true
            }
        }
        etc
    """

    def scrape(self):
        try:
            url = "https://app.vuejobs.com/posts/items?filter\[remote\]=ONLY&limit=-1"

            response = requests.get(url)
            jsonData = response.json()

            jobs = []
            for d in jsonData["data"]:
                job = Job(
                    title=d["title"],
                    description=f"""
                    <div>
                        <h1>Company: {d["organization"]["name"]}</h1>
                        <p>Location: {", ".join([loc["name"] for loc in d["locations"]])}</p>
                        <div>{d["description"]}</div>
                    </div>
                    """,
                    url=d["link"],
                    timestamp=datetime.datetime.fromisoformat(
                        d["published_at"]
                    ).isoformat(),
                )

                jobs.append(job)

            return jobs

        except Exception as err:
            log.exception(err)
            return None
