import re
import time
import requests
from apps.rjobs.scrapper.scrapper_interface import IScrapper
from apps.rjobs.models.job import Job
from common.logger import log


class ScrapeStartupJobsCom(IScrapper):
    """
    Scrapper for: https://startupjobs.com

    """

    def get_job_description_urls(self):
        headers = {
            "accept": "*/*",
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        }

        urls = [
            "https://www.startupjobs.com/jobs?technologies=python,javascript,go&form-of-collaboration=remote",
        ]

        job_description_urls = []
        for url in urls:
            response = requests.get(url, headers=headers)
            """
            <a href="/job/74935/general-manager-for-global-saas-product" class="max-md:first-child:hidden group relative z-10 block border-t-1.5 border-neutral-200 bg-white pb-4 pt-6 first:border-t-0 max-md:px-6 md:border-solid md:hover:border-black" style="order:0;"><div class="absolute inset-x-0 -top-[1.5px] h-[1.5px] bg-neutral-200 transition-all group-first:hidden group-hover:h-0.5 group-hover:bg-blue-700"></div><div class="flex flex-row justify-between gap-3 md:gap-4"><div class="flex h-11 min-w-0 flex-row gap-3 md:gap-4"><img src="https://www.startupjobs.cz/uploads//c8c364b01fed35cce41ab7bfb5d6f74f.png" alt="itrinity, s.r.o." class="mx-auto h-11 shrink-0" style="aspect-ratio:28/15;"><div class="flex h-11 min-w-0 flex-col"><h6 class="flex items-center gap-2 text-base font-semibold -tracking-1"><span class="min-w-0 overflow-hidden truncate">itrinity, s.r.o.</span><!----></h6><div class="label-sm h-5 text-neutral-400">E-commerce</div></div></div><div><button class="group/offer-card-bookmark flex h-11 w-11 items-center justify-center border-1.5 border-solid border-transparent transition-colors md:h-10 md:w-10 md:hover:border-black md:hidden"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="fill-transparent h-6 w-6 transition-colors" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_16019_22573)"><path d="M19 19L11.97 15.5L5 19V3H19V19Z" stroke="black" stroke-width="2" stroke-miterlimit="10" class="stroke-black  group-hover/offer-card-bookmark:stroke-blue-700"></path><path d="M9 7H15" stroke="black" stroke-width="2" stroke-miterlimit="10" class="stroke-black group-hover/offer-card-bookmark:stroke-blue-700 transition-colors"></path></g><defs><clipPath id="clip0_16019_22573"><rect width="16" height="18.62" fill="white" transform="translate(4 2)"></rect></clipPath></defs></svg></button><!----></div></div><div class="mt-4"><span class="inline-block bg-red-500 px-2 py-1 text-sm font-bold leading-none text-white transition-colors md:group-hover:bg-black mr-2 md:hidden">HOT</span><h5 class="label-lg inline transition-colors md:group-hover:text-blue-700">General Manager for global SaaS product 🚀</h5><span class="inline-block bg-red-500 px-2 py-1 text-sm font-bold leading-none text-white transition-colors md:group-hover:bg-black ml-2 align-top max-md:hidden">HOT</span><!----></div><div class="flex flex-row items-center justify-between max-md:-mr-6 max-md:mt-1"><div class="relative w-full overflow-x-hidden"><ul class="no-scrollbar flex list-none flex-row text-sm font-medium -tracking-1 text-neutral-400 transition-colors max-md:overflow-x-auto max-md:pr-6 md:group-hover:text-black [&amp;>li:last-child]:border-none [&amp;>li]:flex-none [&amp;>li]:border-r [&amp;>li]:border-neutral-400"><!----><li class="ml-4 pr-4 first:ml-0">Remote</li><li class="ml-4 pr-4 first:ml-0">Bratislava, Praha</li><li class="ml-4">Full-time</li></ul><div class="absolute inset-y-0 right-0 hidden w-16 bg-gradient-to-l from-white md:block"></div></div><button class="group/offer-card-bookmark flex h-11 w-11 items-center justify-center border-1.5 border-solid border-transparent transition-colors md:h-10 md:w-10 md:hover:border-black ml-2 flex-none max-md:hidden"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="fill-transparent h-6 w-6 transition-colors" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_16019_22573)"><path d="M19 19L11.97 15.5L5 19V3H19V19Z" stroke="black" stroke-width="2" stroke-miterlimit="10" class="stroke-black  group-hover/offer-card-bookmark:stroke-blue-700"></path><path d="M9 7H15" stroke="black" stroke-width="2" stroke-miterlimit="10" class="stroke-black group-hover/offer-card-bookmark:stroke-blue-700 transition-colors"></path></g><defs><clipPath id="clip0_16019_22573"><rect width="16" height="18.62" fill="white" transform="translate(4 2)"></rect></clipPath></defs></svg></button></div></a>
            https://www.startupjobs.com/job/36757/full-stack-developer
            """
            href_matches = re.findall(r'<a href="/job/(.*?)">', response.text)
            href_matches = [
                f"https://www.startupjobs.com/job/{partial_url}"
                for partial_url in href_matches
            ]
            job_description_urls.extend(href_matches)
            time.sleep(0.3)  # trying not to get blocked

        return job_description_urls

    def get_job_title(self, textHTML: str):
        """
        <h1 class="job-title">
            Senior Big Data Engineer
        </h1>
        """
        h1_pattern = re.compile(r'<h1 class="job-title">(.*?)<\/h1>', re.DOTALL)
        match = h1_pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def get_job_description(self, textHTML: str):
        """
        <div class="output-content hidden sm:block">JD</div>
        """
        pattern = re.compile(
            r'<div class="output-content hidden sm:block">(.*?)<\/div>',
            re.DOTALL,
        )
        match = pattern.search(textHTML)
        if match:
            return match.group(1).strip()
        return ""

    def scrape(self):
        try:
            job_description_urls = self.get_job_description_urls()

            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
            }

            jobs = []
            for job_url in job_description_urls:
                response = requests.get(job_url, headers=headers)
                job = Job(
                    title=self.get_job_title(response.text),
                    description=self.get_job_description(response.text),
                    url=job_url,
                )
                jobs.append(job)
                time.sleep(0.5)  # trying not to get blocked

            return jobs

        except Exception as err:
            log.exception(err)
            return None
