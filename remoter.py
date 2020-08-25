import json
import os
import itertools
from datetime import date


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

    # Load websites file
    with open('websites.json') as f:
        websites = json.load(f)

    website_names = list(websites.keys())
    print(f"{len(website_names)} job pages to be parsed!")

    asession = AsyncHTMLSession()

    for idx, site_name in enumerate(website_names):
        
        if site_name.startswith("_"): continue
        
        try:
            asession.run(
                Scrapper(websites, site_name, asession, debug=DEBUG).fetch_jobs
            )
        except Exception as e:
            Jobs.create(
                website=site_name,
                link=websites[site_name]["link"],
                title=str(e)
            )
            print("FAILED:", site_name, websites[site_name]["link"])
            print(str(e))

        if DEBUG:
            break


    with open("latest_update.txt", "w") as f:
        f.write(str(date.today()))

    print("Database updated!")

else:
    print("Already parsed websites today!")
