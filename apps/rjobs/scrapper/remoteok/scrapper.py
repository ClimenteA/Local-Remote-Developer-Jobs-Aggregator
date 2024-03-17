import re
import json
import requests
import datetime
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeRemoteOk(IScrapper):
    """
    Scrapper for: https://remoteok.com

    {
        "job_post_url": "https://remoteok.com/joblistingetc",
        "@context": "http://schema.org",
        "@type": "JobPosting",
        "datePosted": "2024-03-15T20:00:12+00:00",
        "description": "\nThe company\nOutrider is a software company that is automating distribution yards with electric, self-driving trucks. Our system eliminates manual tasks that are hazardous and repetitive while it improves safety and efficiency. Outrider\u2019s mission is to drive the rapid adoption of sustainable freight transportation. We are a private company founded in 2018 and backed by NEA, 8VC, Koch Disruptive Technologies, and other top-tier investors. Our customers are Fortune 200 companies and our autonomous trucks are already running in distribution yards. For more information, visit www.outrider.ai\n\n\nThe role\nOutrider is an ambitious company that aims to solve autonomous vehicles for yard\/warehouse operation. We are building a special electric truck that can achieve complex maneuvers in huge warehouses, among traffic, people and other complicated settings. This is not your generic autonomous vehicle product: we have a specific setting, specific hardware and specific customers.\nWe have gr\n Apply now and work remotely at Outrider",
        "jobBenefits": "\ud83d\udcb0 401(k)\n\ud83c\udf0e Distributed team\n\u23f0 Async\n\ud83e\udd13 Vision insurance\n\ud83e\uddb7 Dental insurance\n\ud83d\ude91 Medical insurance\n\ud83c\udfd6 Unlimited vacation\n\ud83c\udfd6 Paid time off\n\ud83d\udcc6 4 day workweek\n\ud83d\udcb0 401k matching\n\ud83c\udfd4 Company retreats\n\ud83c\udfec Coworking budget\n\ud83d\udcda Learning budget\n\ud83d\udcaa Free gym membership\n\ud83e\uddd8 Mental wellness budget\n\ud83d\udda5 Home office budget\n\ud83e\udd67 Pay in crypto\n\ud83e\udd78 Pseudonymous\n\ud83d\udcb0 Profit sharing\n\ud83d\udcb0 Equity compensation\n\u2b1c\ufe0f No whiteboard interview\n\ud83d\udc40 No monitoring system\n\ud83d\udeab No politics at work\n\ud83c\udf85 We hire old (and young)",
        "baseSalary": {
            "@type": "MonetaryAmount",
            "currency": "USD",
            "value": {
                "@type": "QuantitativeValue",
                "minValue": 65000,
                "maxValue": 110000,
                "unitText": "YEAR"
            }
        },
        "employmentType": "FULL_TIME",
        "directApply": "http://schema.org/False",
        "industry": "Startups",
        "jobLocationType": "TELECOMMUTE",
        "applicantLocationRequirements": {
            "@type": "Country",
            "name": "Anywhere"
        },
        "jobLocation": {
            "address": {
                "@type": "PostalAddress",
                "addressCountry": "Anywhere",
                "addressRegion": "Anywhere",
                "streetAddress": "Anywhere",
                "postalCode": "Anywhere",
                "addressLocality": "Anywhere"
            }
        },
        "title": "Senior Engineer Deep Learning",
        "image": "https:\/\/remoteok.com\/assets\/img\/jobs\/227bea9816cfe4c0c8a530ee4b2ded791710532813.png",
        "occupationalCategory": "Senior Engineer Deep Learning",
        "workHours": "Flexible",
        "validThrough": "2024-06-13T20:00:12+00:00",
        "hiringOrganization": {
            "@type": "Organization",
            "name": "Outrider",
            "url": "https:\/\/remoteok.com\/outrider",
            "sameAs": "https:\/\/remoteok.com\/outrider",
            "logo": {
                "@type": "ImageObject",
                "url": "https:\/\/remoteok.com\/assets\/img\/jobs\/227bea9816cfe4c0c8a530ee4b2ded791710532813.png"
            }
        }
    }

    """

    @staticmethod
    def clean_json_string(text):
        text = re.sub(r"\n", "", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text

    def parseHTML(self, textHTML: str):
        """
        From raw html response from url we extract the json from script tag and url from tr tag.
        We add job_post_url to exsiting json.
        """
        tr_href_matches = re.findall(r'<tr .*?data-href="(.*?)"', textHTML)
        script_json_matches = re.findall(
            r'<script type="application/ld\+json">(.*?)</script>', textHTML, re.DOTALL
        )

        rawjobs = []
        for tfhref, scriptjsonstr in zip(tr_href_matches, script_json_matches):
            try:
                job = json.loads(self.clean_json_string(scriptjsonstr))
                job["job_post_url"] = "https://remoteok.com/" + tfhref
                rawjobs.append(job)
            except Exception as err:
                log.exception(err)

        return rawjobs

    def scrape(self):
        try:
            url = "https://remoteok.com/?tags=engineer&location=region_EU,Worldwide&order_by=date&action=get_jobs"
            response = requests.get(url)
            rawjsonlist = self.parseHTML(response.text)

            jobs = []
            for d in rawjsonlist:
                job = Job(
                    title=d["title"],
                    description=f"""
                    <div>
                    <p>{d["description"]}</p>
                    <p>Benefits: {d["jobBenefits"]}</p>
                    <p>Location: {d["applicantLocationRequirements"]["name"]}</p>
                    </div>
                    """,
                    url=d["job_post_url"],
                    timestamp=datetime.datetime.fromisoformat(
                        d["datePosted"]
                    ).isoformat(),
                )
                jobs.append(job)

            return jobs

        except Exception as err:
            log.exception(err)
            return None
