from datetime import date
from urllib.parse import urljoin
from models import Jobs


class Scrapper:
    """
        - Get link to job description by filtering all links in the page by root link
        Ex: https://remotive.io/remote-jobs/software-dev/some-job-id-here 
        with request_html module > r.html.absolute_links func
        - Get job details based on the css selectors provided

    """

    def __init__(self, site_inital_data, previous_links, async_session, debug=True):
        
        """
            site_inital_data: website name, root link, css selectors
            previous_links: already saved job description links from database
            async_session: requests_html async sesstion
            debug: if true get only first link from the website

        """

        self.site_name = site_inital_data["name"]
        self.root_link = site_inital_data["link"]
        self.selectors = site_inital_data["selectors"]
        self.current_links = []
        self.previous_links = previous_links 
        self.asession = async_session
        self.debug = debug
        

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


    async def get_links_to_job_description(self):
        """ 
            Get a list of links to the full job description
        """

        r = await self.asession.get(self.root_link)
        await r.html.arender()

        action_divs = r.html.find(self.selectors["action"])

        action_links = []
        for idx, div in enumerate(action_divs):      
            
            link = await self.get_job_description_link(idx, div)
            
            if link == "skip": 
                continue
            if not link.startswith(self.root_link):
                continue
            if link in self.previous_links:
                continue
            if link in self.current_links:
                continue

            self.current_links.append(link)
            
            if self.debug:
                break

        #Make sure that there are no duplicates
        self.current_links = list(set(self.current_links))
        
    
    async def data_from_selector(self, response, selector, html=True):

        try:
            if html:
                data = response.html.find(selector, first=True).html
            else:
                data = response.html.find(selector, first=True).text
            if isinstance(data, tuple):
                data = list(data)[0]
        except:
            data = "Not found"
        
        return data

  
    async def fetch_jobs(self):

        #Save to self.current_links links to job description
        await self.get_links_to_job_description() 

        #Get job details for each job description link
        for job_link in self.current_links:
            
            r = await self.asession.get(job_link)
            
            Jobs.create(
                website     = self.site_name, 
                link        = job_link, 
                title       = await self.data_from_selector(r, self.selectors["title"], False), 
                company     = await self.data_from_selector(r, self.selectors["company"], False),
                description = await self.data_from_selector(r, self.selectors["description"]),
                status      = "new"
            )
            
            print("SAVED:", job_link)

            if self.debug:
                break

        print(f"\n{self.site_name} - DONE\n")


















class Scrapper_old:
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



