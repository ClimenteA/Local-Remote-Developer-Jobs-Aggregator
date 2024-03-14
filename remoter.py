import json
import os
from datetime import date
import traceback

DEBUG = True

latest_update = None
if os.path.isfile("latest_update.txt"):
    with open("latest_update.txt", "r") as f:
        latest_update = f.read()
        print("Latest database update was on:", latest_update)


if latest_update != str(date.today()):
    print("Fetching latest jobs...")
    from requests_html import AsyncHTMLSession
    from scrapper import Scrapper

    asession = AsyncHTMLSession()

    # Load websites file
    with open("websites.json") as f:
        websites = json.load(f)

    website_names = [w for w in list(websites.keys()) if not w.startswith("_")]
    print(f"{len(website_names)} job pages to be parsed!")

    for site_data in website_names:
        try:
            asession.run(
                Scrapper(websites, site_data, asession, debug=DEBUG).fetch_jobs
            )
        except Exception as e:
            print("FAILED:", site_data)
            print(e, traceback.format_exc())

        if DEBUG:
            break

    with open("latest_update.txt", "w") as f:
        f.write(str(date.today()))

    print("Database updated!")

else:
    print("Already parsed websites today!")
