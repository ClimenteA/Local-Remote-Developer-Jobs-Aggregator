import requests
import datetime
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeRemotive(IScrapper):
    """

    Scrapper for: https://remotive.com/

    Using the api provided that returns:

    {
        "00-warning": "Remotive main domain moved to remotive.com ! Please make your API calls on remotive.com/api/remote-jobs instead of remotive.io now ;) Legacy endpoint remotive.io/api/remote-jobs will be terminated in June 2022. Thank you!",
        "0-legal-notice": "Legal warning - Hey, thanks for using Remotive's API, we appreciate it! Please note that API documentation and access is granted so that developers can share our jobs further. Please do not submit Remotive jobs to third Party websites, including but not limited to: Jooble, Neuvoo, Google Jobs, LinkedIn Jobs. Please link back to the URL found on Remotive AND mention Remotive as a source in order to Remotive to get traffic from your listing. If you don't do that, we'll terminate your API access, sorry! Jobs displayed are delayed by 24 hours, the goal being that jobs are attributed to Remotive on various platforms. Displaying our jobs in order to collect signups/email addresses to show a listing constitutes a breach of our terms of services. We offer a private, paid-for API, please email us at hello(at)remotive(dot)io for more information (starting budget is $5k/mo). Please find out terms of services on https://remotive.com/api-documentation. Please note that there is absolutely no need to request Remotive Job data too frequently. Typically, you only need to GET Remotive job data through this API a couple of times a day (we advise max. 4 times a day). Our data is not changing much faster than that anyway. Note that excessive requests will be blocked. Many thanks (Rodolphe & the Remotive team!)",
        "job-count": 280,
        "jobs": [
            {
                "id": 1900353,
                "url": "https://remotive.com/remote-jobs/software-dev/senior-backend-engineer-gn-1900353",
                "title": "Senior Backend Engineer (gn)",
                "company_name": "Cybus",
                "company_logo": "https://remotive.com/job/1900353/logo",
                "category": "Software Development",
                "tags": ["docker", "javascript", "node.js"],
                "job_type": "full_time",
                "publication_date": "2024-03-15T14:51:13",
                "candidate_required_location": "Germany",
                "salary": "",
                "description": '<p><strong>About Cybus</strong></p>\n<p>With a common goal to drive innovation in the manufacturing industry using the proven principles of IoT technologies, our team has been growing steadily since 2015. We are IoT experts, experienced programmers and engineers and overall experts in various fields, which enables us to empower factories to gain long-term independence from manufacturers and vendors.</p>\n<p>In a nutshell: Cybus\' IIoT software product Connectware is an on-premise solution that provides a communication layer enabling our customers in the manufacturing industry to connect their machines and make smart factories a reality.</p>\n<p>For what? More efficiency, less energy and fewer emissions.</p>\n<p><strong>Driven by Independence. Inspired by Creativity and Collaboration.</strong></p>\n<p>Join our team as <strong>Senior Backend Engineer (gn)</strong> and design, develop and maintain our cutting-edge microservice-oriented software product that our customers engage in production critical environments.</p>\n<div class="h2">Tasks</div>\n<p>As <strong>Senior Backend Engineer (gn),</strong> you design, develop and maintain our cutting-edge microservice-oriented software product as a part of an experienced agile team.</p>\n<ul style="">\n<li style="">Participate in engineering and actively improving our IIoT software product.</li>\n<li style="">Design and develop a microservice-oriented industrial software that interconnects modern smart factories.</li>\n<li style="">Work with our application core technologies, which is Node.js and Go and modern broker technologies</li>\n<li style="">Troubleshoot and debug software problems</li>\n<li style="">Write and maintain documentation for software applications</li>\n</ul>\n<div class="h2">Requirements</div>\n<p><strong>Qualification</strong></p>\n<ul style="">\n<li style="">Minimum 5 years of experience in <strong>designing and building backend systems</strong> ideally in an <strong>event driven micro-service</strong> environment</li>\n<li style="">Highly proficient in <strong>Golang</strong> and proficient in <strong>Node.js</strong> for backend development</li>\n<li style="">Good knowledge of <strong>Linux</strong> and <strong>Docker</strong>.</li>\n<li style="">Familiarity developing <strong>custom protocols over TCP.</strong></li>\n<li style="">Familiarity with <strong>message broker technologies</strong> like MQTT, NATS or other</li>\n</ul>\n<p>Bonus points for</p>\n<ul style="">\n<li style="">Experience in developing solutions for Industrial IoT applications.</li>\n<li style="">Understanding of TCP/IP networks.</li>\n</ul>\n<div class="h2">Benefits</div>\n<p><strong>That\'s what we do to make you happy:</strong></p>\n<ul style="">\n<li style="">We are a company with flat hierarchies and plenty of freedom to make your own decisions and assume your own area of responsibility.</li>\n<li style="">Diversity, mutual respect and a strong sense of togetherness are essential for us. We grow together and meet each other at eye level.</li>\n<li style="">We offer an appealing and varied job where you can make things happen without a lot of bureaucracy.</li>\n<li style="">A strong sense of community and regular team events.</li>\n<li style="">We offer continuous training - adapted to your skills and interests.</li>\n<li style="">A workplace with a feel-good atmosphere: this includes a professional coffee machine, sweet snacks and fresh fruit, but also an after-work drink or beer.</li>\n<li style="">Reliable work-life balance with flexible working hours and 30 days of holiday per year and a one-off additional holiday of 10, 15 or 20 days after 3, 4 or 5 years of employment with the company</li>\n<li style="">Flex Holidays: Use up to 5 of your 30 vacation days as flexible leave, either for an extended break or for financial benefits</li>\n<li style="">Childcare Support: Up to 100 EUR subsidy for childcare costs per child of preschool age</li>\n<li style="">Monthly allowance of 50 EUR for meals, sports, bike leasing or public transport</li>\n<li style="">Attractive pension plan with subsidised direct insurance and a fully financed provident fund is of course also part of the package.</li>\n<li style="">You decide where you are most productive: whether completely at home, under palm trees, during your workation or at one of our offices in Hamburg Eimsbüttel or in Berlin between Zoo station and U Wittenbergplatz.</li>\n</ul>\n<p>We value diversity and therefore welcome all applications - regardless of gender, nationality, ethnic and social origin, religion/belief, disability, age, sexual orientation and identity.</p>\n<p><strong>We look forward to receiving your application!</strong></p>\n<div class="h1">About the company</div>\n<p>Building the Data Infrastructure for the Industrial IoT World. Driven by independence. Inspired by creativity and collaboration.</p>\n<img src="https://remotive.com/job/track/1900353/blank.gif?source=public_api" alt=""/>',
            },
            etc
        ]
    }

    """

    def scrape(self):
        try:
            url = "https://remotive.com/api/remote-jobs?category=software-dev"

            response = requests.get(url)
            jsonData = response.json()

            jobs = []
            for d in jsonData["jobs"]:
                job = Job(
                    title=d["title"],
                    description=f"""
                    <div>
                        <h1>Company: {d["company_name"]}</h1>
                        <p>{", ".join(d["tags"])}</p>
                        <p>Location: {d["candidate_required_location"]}</p>
                        <div>{d["description"]}</div>
                    </div>
                    """,
                    url=d["url"],
                    timestamp=datetime.datetime.fromisoformat(
                        d["publication_date"]
                    ).isoformat(),
                )

                jobs.append(job)

            return jobs

        except Exception as err:
            log.exception(err)
            return None
