import asyncio
import json
from playwright.async_api import async_playwright, Page


def save_jobs(name: str, jobs: list[dict]):
    with open(f"{name}.json", "w") as f:
        f.write(json.dumps(jobs))
    return name


async def get_remotive_jobs(page: Page):
    base_urls = [
        "https://remotive.com/remote-jobs/software-dev?query=Python",
        "https://remotive.com/remote-jobs/software-dev?query=Javascript",
        "https://remotive.com/remote-jobs/software-dev?query=Golang",
    ]

    for base_url in base_urls:
        await page.goto(base_url, wait_until="domcontentloaded")

        job_cards = await page.locator("css=.job-tile-title").all()

        jobs = []
        for card in job_cards:
            href = await card.locator("css=a").get_attribute("href")
            job_title = await card.locator("css=a").inner_text()
            job_url = "https://remotive.com" + href
            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("remotive", jobs)


async def get_remoteok_jobs(page: Page):
    base_urls = [
        "https://remoteok.com/remote-python-jobs?order_by=date",
        "https://remoteok.com/remote-javascript-jobs?order_by=date",
        "https://remoteok.com/remote-golang-jobs?order_by=date",
    ]

    for base_url in base_urls:
        await page.goto(base_url, wait_until="domcontentloaded")

        job_cards = await page.locator(
            "css=.company.position.company_and_position"  # error here
        ).all()

        jobs = []
        for card in job_cards:
            href = await card.locator("css=a").get_attribute("href")
            job_title = await card.locator("css=a").inner_text()
            job_url = "https://remoteok.com" + href
            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("remotive", jobs)


async def get_ejobs_jobs(page: Page):
    base_urls = [
        "https://www.ejobs.ro/locuri-de-munca/remote/it-software/mid-level,senior-level/it---telecom/sort-publish",
    ]

    for base_url in base_urls:
        await page.goto(base_url, wait_until="domcontentloaded")

        job_cards = await page.locator("css=.JCContentMiddle").all()

        jobs = []
        for card in job_cards:
            href = await card.locator("css=a").get_attribute("href")
            job_title = await card.locator("css=a").inner_text()
            job_url = "https://www.ejobs.ro" + href
            jobs.append({"title": job_title, "url": job_url, "source": base_url})

    return save_jobs("ejobs", jobs)


JOB_FUNCS = [
    get_remotive_jobs,
    get_remoteok_jobs,
    get_ejobs_jobs,
]


async def main(job_funcs: list[callable]):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        for func in job_funcs:
            await func(page)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main(JOB_FUNCS))
