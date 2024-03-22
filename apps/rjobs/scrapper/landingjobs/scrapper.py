import requests
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeLandingJobs(IScrapper):
    """
    Scrapper for: https://landing.jobs

    "offers": [
        {
            "id": 18160,
            "title": "Full-Stack Software Engineer (NestJS/ Angular)",
            "slug": "full-stack-software-engineer-nestjs-angular",
            "dismiss_url": "/jobs/full-stack-software-engineer-nestjs-angular/dismissal",
            "country_code": "PT",
            "company_logo_url": "https://storage.landing.jobs/5JFVqDTQ7g5ofETpSxWTjqMt",
            "company_url": "https://landing.jobs/at/iownit",
            "company_slug": "iownit",
            "company_name": "Iownit",
            "company_id": 5541,
            "contract_type": "Permanent",
            "experience_level": "Intermediate",
            "experience_min": 3,
            "experience_max": null,
            "is_new": true,
            "job_classes": " ld-new",
            "location": "Lisbon, Portugal",
            "remote": true,
            "remote_label": "Eventual restrictions regarding residency or citizenship. You may specify timezone restrictions and office locations (exceptionally).",
            "global_remote": false,
            "full_remote": true,
            "partial_remote": false,
            "office_locations": [
                {
                    "city": "Lisbon",
                    "country_code": "PT",
                    "google_place_id": "ChIJO_PkYRozGQ0R0DaQ5L3rAAQ",
                    "label": "Lisbon, Portugal"
                }
            ],
            "on_multiple_locations?": false,
            "timezone_tolerance": "UTC -01:00 — UTC +00:00",
            "onsite_job": false,
            "published_at": "2024-03-13",
            "salary": "€30.200 - €45.300",
            "industry": "Technology",
            "company_size": "21 to 50 people",
            "remote_tooltip": "Remote",
            "skills": [
                {
                    "name": "Node.js",
                    "canon_id": 198
                },
                {
                    "name": "NestJS",
                    "canon_id": 62552
                },

            ],
            "url": "https://landing.jobs/at/iownit/full-stack-software-engineer-nestjs-angular",
            "hiring_bonus": null
        }

        fetch("https://landing.jobs/graphql", {
        "headers": {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,ro;q=0.8",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"122\", \"Not(A:Brand\";v=\"24\", \"Microsoft Edge\";v=\"122\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Linux\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "x-csrf-token": "wRvubAQEeC/bNWH3rQ5xSu0LbaOZgOUW1qvDrmO/eSveRwkH5yzh6RAlY1LfWXcs1EdgdCPoKExwhUZmsOO2vg=="
        },
        "referrer": "https://landing.jobs/at/iownit/full-stack-software-engineer-nestjs-angular",
        "referrerPolicy": "strict-origin-when-cross-origin",
        "body": "{
            \"operationName\":null,
            \"variables\":{\"id\":\"5541\"},
            \"query\":\"query ($id: ID!) {\\n
            company(id: $id)
            {\\n    averageHiringProcess(id: $id)
              {\\n      companyAvg\\n      marketAvg\\n      __typename\\n    }\\n    coverPhotoUrl\\n    description\\n    id\\n    logoUrl\\n    name\\n    slug\\n    shortPitch\\n    __typename\\n  }\\n  jobs(companyId: $id) {\\n    nodes {\\n      location\\n      id\\n      salary\\n      title\\n      locationIcon\\n      remotePolicy\\n      officeLocations {\\n        googlePlaceId\\n        city\\n        countryCode\\n        label\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n  currentUser {\\n    id\\n    type\\n    __typename\\n  }\\n  person {\\n    applications(companyId: $id) {\\n      id\\n      jobId\\n      state\\n      stateForCandidate\\n      inDraftStates\\n      submittedAt\\n      __typename\\n    }\\n    companySubscriptions(companyId: $id) {\\n      id\\n      __typename\\n    }\\n    __typename\\n  }\\n  user {\\n    bookmarks {\\n      id\\n      jobId\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n\"}",
        "method": "POST",
        "mode": "cors",
        "credentials": "include"
        });

    """

    def scrape(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
            }

            url = "https://landing.jobs/jobs/search.json?page=1&gr=true&fr=true&c%5B%5D=1&c%5B%5D=2&c%5B%5D=3&match=all&pd=7&hd=false&t_co=false&t_st=false"

            response = requests.get(url, headers=headers)
            rawjsonlist = [d for d in response.json() if d["full_remote"]]

            jobs = []
            for d in rawjsonlist:
                # Loads async
                # response = requests.post(d["url"], headers=headers)
                # details = response.json()

                job = Job(
                    title=d["title"],
                    description="""
                    <div>
                    __TODO__
                    </div>
                    """,
                    url=d["url"],
                )

                jobs.append(job)
                # time.sleep(0.5)  # trying not to get blocked

            return jobs

        except Exception as err:
            log.exception(err)
            return None
