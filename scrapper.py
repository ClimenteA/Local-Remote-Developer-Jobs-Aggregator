from datetime import date
from urllib.parse import urljoin
from models import Jobs

# TODO

# some site use an token for each job details page - this causes duplicates
# try to find action links using the startswith pattern like "https://sitename.com/jobs/etc"
# split assesion in 2 one for getting job description links and
# one for getting the job title, job description, company, date etc

class Scrapper:
    """
        Scrape latest remote jobs using data from websites.json
        ...
        {
            "website_name": {
            "name": "website_name",
            "link": "root website link",
            "selectors": {
                "action": "css selector for link to job description",
                "title": "css selector for job title",
                "company": "css selector for company name",
                "description": "css selector for job description"
                }        
            }
        }, etc
    """

    def __init__(self, site_inital_data, job_description_links, async_session, debug=True):
        
        """
            site_inital_data: website name, root link, css selectors
            job_description_links: already saved job description links from database
            async_session: requests_html async sesstion
            debug: if true get only first link from the website

        """

        self.site_name = site_inital_data["name"]
        self.link = site_inital_data["link"]
        self.selectors = site_inital_data["selectors"]
        self.job_description_links = job_description_links 
        self.session = async_session
        self.debug = debug
        self.saved_job_description_links = []
        

    async def text_from_selector(self, response, selector):

        try:
            text_data = response.html.find(selector, first=True).text
            if isinstance(text_data, tuple):
                text_data = list(text_data)[0]
        except:
            text_data = "Not found"
        
        return text_data


    async def get_job_description_link(self, idx, div):

        if "remotive" in self.site_name:
            action_link = urljoin(self.link, div.attrs["data-url"]) 
        elif "jsremotely" in self.site_name:
            if idx == 0: return "skip"
            action_link = urljoin(self.link, div.attrs["href"])
        else:
            action_link = div.find('a', first=True)
            action_link = list(action_link.absolute_links)[0] 

        return action_link


    async def links_to_job(self):
        """ Get a list of links to the full job description """
        
        r = await self.session.get(self.link)
        await r.html.arender()
        
        action_divs = r.html.find(self.selectors["action"])

        # print("Action divs:", action_divs)

        job_details_links =[]
        for idx, div in enumerate(action_divs):
            
            action_link = await self.get_job_description_link(idx, div)

            if action_link == "skip": continue

            if action_link not in self.job_description_links:
                job_details_links.append(action_link)
                # print("Job description link:", action_link)
            else:
                print("Duplicate: ", action_link)
            
            if self.debug:
                break

        return job_details_links


    async def fetch_jobs(self):
        
        print("Getting data from", self.link)

        job_details_links = await self.links_to_job()
        
        for job_link in job_details_links:
            # Prevent duplicate links from the same site
            if job_link not in self.saved_job_description_links:

                self.saved_job_description_links.append(job_link)
            
                r = await self.session.get(job_link)
                
                Jobs.create(
                    website     = self.site_name, 
                    link        = job_link, 
                    title       = await self.text_from_selector(r, self.selectors["title"]), 
                    company     = await self.text_from_selector(r, self.selectors["company"]),
                    description = await self.text_from_selector(r, self.selectors["description"])
                )
                
                print("SAVED:", job_link)
                

            if self.debug:
                break

        
        print(f"\n{self.site_name} - DONE\n")



