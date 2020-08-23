from datetime import date
from urllib.parse import urljoin
from models import Jobs


class Scrapper:
    """
        - Get link to job description by filtering all links in the page by root link
        Ex: https://remotive.io/remote-jobs/software-dev/some-job-id-here 
        with request_html module > r.html.absolute_links func
        - Get job details based on the css selectors provided

        Schema:

        "remotive_dev": {
                    "name": "remotive_dev",
                    "link": "https://remotive.io/remote-jobs/software-dev", #root link to job board
                    "selectors": {
                        "action": "css selector for element that contains the link to job description",
                        "title": "css selector for job title",
                        "company": "css selector for company name",
                        "description": "css selector for job description"
                    }
                },

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
            action_link = urljoin(self.root_link, div.attrs["data-url"]) 
        elif "jsremotely" in self.site_name:
            if idx == 0: return "skip"
            action_link = urljoin(self.root_link, div.attrs["href"])
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

        for idx, div in enumerate(action_divs):      
            
            link = await self.get_job_description_link(idx, div)
            
            if link == "skip": 
                print("Skipped:", link)
                continue
            if link in self.previous_links:
                print("Duplicated link:", link)
                continue
            if link in self.current_links:
                print("Already addded:", link)
                continue
            if "remote-companies" in link:
                continue


            print("Waiting to save:", link)

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
