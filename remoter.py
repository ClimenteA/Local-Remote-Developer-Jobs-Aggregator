import json
import os
import itertools
from datetime import date


def grouper(size, iterable):
    it = iter(iterable)
    while True:
        group = list(itertools.islice(it, None, size))
        if not group:
            break
        yield group


DEBUG = False

latest_update = None
if os.path.isfile("latest_update.txt"):
    with open("latest_update.txt", "r") as f:
        latest_update = f.read()
        print("Latest database update was on:", latest_update)


if latest_update != str(date.today()):

    print("Fetching latest jobs...")
    from requests_html import AsyncHTMLSession
    from scrapper import Scrapper
    from models import Jobs

    asession = AsyncHTMLSession()

    # Load websites file
    with open('websites.json') as f:
        websites = json.load(f)

    website_names = [w for w in list(websites.keys()) if not w.startswith("_")]
    print(f"{len(website_names)} job pages to be parsed!")

    # Size depends on the number of websites added in websites.json
    # If more added then assestion.run funcs must be modified to avoid an index error
    website_names_grouped = list(grouper(size=8, iterable=website_names))
    
    for site_names_grouped in website_names_grouped:
        print(f"\nWorking on group: {site_names_grouped}\n")
        try:
            asession.run(
                Scrapper(websites, site_names_grouped[0], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[1], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[2], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[3], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[4], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[5], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[6], asession, debug=DEBUG).fetch_jobs,
                Scrapper(websites, site_names_grouped[7], asession, debug=DEBUG).fetch_jobs,
            )
        except Exception as e:
            print("FAILED:", site_names_grouped)
            print(str(e))

        if DEBUG:
            break


    with open("latest_update.txt", "w") as f:
        f.write(str(date.today()))

    print("Database updated!")

else:
    print("Already parsed websites today!")

