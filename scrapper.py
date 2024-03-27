import json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Page


def save_jobs(name: str, jobs: list[dict]):
    with open(f"./raw_jobs/{name}.json", "w") as f:
        f.write(json.dumps(jobs))
    return name


def get_remotive_jobs(page: Page):
    base_urls = [
        "https://remotive.com/remote-jobs/software-dev?query=Python",
        "https://remotive.com/remote-jobs/software-dev?query=Javascript",
        "https://remotive.com/remote-jobs/software-dev?query=Golang",
    ]

    jobs = []
    common_url = "/remote-jobs/software-dev"
    for base_url in base_urls:
        page.goto(base_url, wait_until="domcontentloaded")

        html_doc = page.content()
        soup = BeautifulSoup(html_doc, "html.parser")

        for link in soup.find_all("a"):
            job_url = link.get("href")

            if job_url is None:
                continue

            if not job_url.startswith(common_url):
                continue

            if not len(job_url) > len(common_url):
                continue

            spans = link.find_all("span")

            if len(spans) == 0:
                continue

            job_url = "https://remotive.com" + job_url
            job_title = spans[0].get_text()
            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("remotive", jobs)


def get_remoteok_jobs(page: Page):
    base_urls = [
        "https://remoteok.com/remote-python-jobs?order_by=date",
        "https://remoteok.com/remote-javascript-jobs?order_by=date",
        "https://remoteok.com/remote-golang-jobs?order_by=date",
    ]

    jobs = []
    common_url = "/remote-jobs"
    for base_url in base_urls:
        page.goto(base_url, wait_until="domcontentloaded")

        html_doc = page.content()
        soup = BeautifulSoup(html_doc, "html.parser")

        for link in soup.find_all("a"):
            job_url = link.get("href")

            if job_url is None:
                continue

            if not job_url.startswith(common_url + "/"):
                continue

            h2s = link.find_all("h2")

            if len(h2s) == 0:
                continue

            job_title = h2s[0].get_text()
            job_url = "https://remoteok.com" + job_url

            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("remoteok", jobs)


def get_ejobs_jobs(page: Page):
    """
    "https://www.ejobs.ro/locuri-de-munca/remote/it-software/mid-level,senior-level/it---telecom/sort-publish",
    """
    # not scrapable


def get_vuejobs_jobs(page: Page):
    base_urls = ["https://vuejobs.com/jobs"]

    jobs = []
    common_url = "/jobs"
    for base_url in base_urls:
        print("loading page")
        page.goto(base_url, wait_until="domcontentloaded")

        print("page loaded")
        # selector="css=#headlessui-switch-49"
        elem = page.get_by_label("Remote", exact=True)

        print("located:", elem.text_content, elem.is_checked())

        elem.check()

        print("located:", elem.text_content, elem.is_checked())

        print("checked, waiting to load")
        page.wait_for_load_state("networkidle")
        print("done")

        html_doc = page.content()
        soup = BeautifulSoup(html_doc, "html.parser")

        for link in soup.find_all("a"):
            job_url = link.get("href")

            if job_url is None:
                continue

            if not job_url.startswith(common_url + "/"):
                continue

            titles = link.find_all("div.font-display.text-lg.leading-tight.font-bold")

            if len(titles) == 0:
                continue

            job_title = titles[0].get_text()
            job_url = "https://vuejobs.com/jobs" + job_url

            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("vuejobs", jobs)


JOB_FUNCS = [
    # get_remotive_jobs,
    # get_remoteok_jobs,
    get_vuejobs_jobs,
]


def main(job_funcs: list[callable]):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        for func in job_funcs:
            func(page)

        browser.close()


if __name__ == "__main__":
    main(JOB_FUNCS)
