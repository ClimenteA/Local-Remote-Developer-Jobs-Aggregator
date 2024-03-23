import time
import requests
import datetime
from ..scrapper_interface import IScrapper, Job
from common.logger import log


class ScrapeDevjob(IScrapper):
    """
    Scrapper for: https://devjob.ro

    [
        {
            "_id": "6522cffa15225fa528c2089e",
            "jobUrl": "CODEMELT-Senior-Developer-Django-and-Python",
            "isFullRemote": true,
            "isPartner": false,
            "isPaused": false,
            "companyId": "647490c7db0bc083f25165f2",
            "longitude": 26.0452703,
            "latitude": 44.4172128,
            "cityCategory": "Bucuresti",
            "tier": "basic",
            "logoImg": "codemelt-logo-1685361324056.jpg",
            "activeFrom": "2023-10-08T00:00:00.000+03:00",
            "companyWebsiteLink": "codemelt.com",
            "candidateContactWay": "Email",
            "company": "CODEMELT",
            "address": "Vladeasa 7",
            "actualCity": "Bucuresti",
            "postalCode": "061672",
            "companyType": "Services",
            "companySize": "<50",
            "language": "English",
            "perkKeys": [
                "wweek40",
                "remote3day",
                "startupculture"
            ],
            "offerStockOrBonus": false,
            "name": "Senior Developer (Django and Python)",
            "jobType": "Full-Time",
            "expLevel": "Senior",
            "annualSalaryFrom": 9000,
            "annualSalaryTo": 13000,
            "techCategory": "Python",
            "technologies": [
                "Django",
                "Python",
                "JavaScript",
                "CSS"
            ],
            "filterTags": [
                "CI/CD",
                "CSS",
                "Django",
                "Git",
                "NestJS",
                "Security",
                "Web",
                "JavaScript",
                "Python"
            ]
        }
    ]

    On details:
    {
        "_id": "6522cffa15225fa528c2089e",
        "isDisabledOrOutdated": false,
        "jobUrl": "CODEMELT-Senior-Developer-Django-and-Python",
        "isFullRemote": true,
        "isPartner": false,
        "isPaused": false,
        "companyId": "647490c7db0bc083f25165f2",
        "longitude": 26.0452703,
        "latitude": 44.4172128,
        "cityCategory": "Bucuresti",
        "tier": "basic",
        "logoImg": "codemelt-logo-1685361324056.jpg",
        "activeFrom": "2023-10-08T00:00:00.000+03:00",
        "companyWebsiteLink": "codemelt.com",
        "candidateContactWay": "Email",
        "company": "CODEMELT",
        "address": "Vladeasa 7",
        "actualCity": "Bucuresti",
        "postalCode": "061672",
        "emailAddressForApplications": "alexandra@codemelt.com",
        "companyType": "Services",
        "companySize": "<50",
        "language": "English",
        "perks": [],
        "perkKeys": [
            "wweek40",
            "remote3day",
            "startupculture"
        ],
        "allowDirectContact": false,
        "offerStockOrBonus": false,
        "metScrum": false,
        "metCodeReviews": true,
        "metPairProgramm": false,
        "metUnitTests": false,
        "metIntegrationTests": false,
        "metBuildServer": false,
        "metStaticCodeAnalysis": false,
        "metVersionControl": true,
        "metTesters": true,
        "metTimeTracking": true,
        "description": "We are a young software development team based in Bucharest.",
        "name": "Senior Developer (Django and Python)",
        "jobType": "Full-Time",
        "expLevel": "Senior",
        "annualSalaryFrom": 9000,
        "annualSalaryTo": 13000,
        "techCategory": "Python",
        "technologies": [
            "Django",
            "Python",
            "JavaScript",
            "CSS"
        ],
        "filterTags": [
            "CI/CD",
            "CSS",
            "Django",
            "Git",
            "NestJS",
            "Security",
            "Web",
            "JavaScript",
            "Python"
        ],
        "requirementsMustTextArea": "Bachelor's degree in Computer Science, Software Engineering, or a related field (or equivalent experience).\nExtensive experience and expertise in Django, Phyton, and CSS (minimum of 5 years experience)\nProven track record of delivering complex web applications using Django and Phyton, demonstrating the ability to design and build highly scalable, reusable, and performant components and architectures.\nIn-depth knowledge of advanced Django and Phyton concepts, state management patterns, performance optimizations, and design patterns.\nDeep understanding of NestJS decorators, modules, middleware, and dependency injection.\nStrong knowledge of software engineering principles, including software design patterns, SOLID principles, and testing methodologies.\nExceptional problem-solving and debugging skills, with a keen eye for detail and a drive for continuous improvement.\nExcellent communication, collaboration, and leadership abilities, with a proven ability to mentor and guide junior team members.\nDemonstrated ability to thrive in a fast-paced, agile environment, managing multiple projects and priorities effectively.\nStrong understanding of version control systems, preferably Git, and experience with CI/CD pipelines.\nPassion for staying up to date with the latest industry trends and technologies, and a constant desire to learn and grow.",
        "requirementsNiceTextArea": "Competitive salary & contract flexibility (remote work)\nFull-time flexible schedule (40 working hours per week)",
        "responsibilitiesTextArea": "Lead and guide the development and maintenance of complex web applications using Django and Phyton.\nCollaborate closely with the development team, providing technical leadership and architectural expertise to design robust user interfaces and application components.\nDrive the implementation of best practices, coding standards, and software development methodologies to ensure the delivery of high-quality, scalable, and performant solutions.\nOptimize applications for maximum speed, scalability, and usability, leveraging advanced techniques and technologies.\nWork closely with cross-functional teams, including designers and product managers, to translate business requirements into technical solutions.\nMentor and coach junior and mid-tier developers, sharing your knowledge, expertise, and industry best practices to foster their growth and development.\nConduct comprehensive code reviews, offer constructive feedback, and ensure adherence to coding standards, security practices, and performance optimizations.\nStay at the forefront of emerging technologies, frameworks, and industry trends related to Django, CSS and Phyton, and web development as a whole.\nCollaborate with stakeholders to gather requirements, provide technical guidance, and drive the successful implementation of new features and enhancements.\nOversee and participate in refactoring initiatives, continuously improving the codebase for better maintainability, scalability, and testability.",
        "createdAt": "2023-10-08T15:51:22.892Z",
        "updatedAt": "2023-10-08T15:51:22.892Z",
        "__v": 0
    }

    """

    def scrape(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43"
            }
            url = "https://devjob.ro/api/jobsLight"

            response = requests.get(url, headers=headers)
            rawjsonlist = [d for d in response.json() if d["isFullRemote"]]

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
