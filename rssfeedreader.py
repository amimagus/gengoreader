import json

# import requests
# import schedule
from bs4 import BeautifulSoup
from plyer import notification

# import time


def main():  # Scrapes rss feed for titles and links of currently available translation jobs

    newjobs = []

    items = read()
    for item in items:
        # title = item.title.text
        link = item.link.text
        # print(f"Title: {title}\n\nLink: {link}\n\n-----------------------\n")

        # If return value of write is True, add to list. If false, do nothing.
        if write(link):
            newjobs.append(link)

    # Notify user of list of new jobs. Want to change to email instead of desktop notification.
    notification.notify(
        title="NEW JOB!",
        message=f"{newjobs}",
        app_icon=None,
        timeout=10,
    )

    # print("END OF AVAILABLE JOBS\n")


# read gets all available jobs and sanitizes them
def read():
    # url = requests.get(
    #     "https://gengo.com/rss/available_jobs/57c56531c6ec0e741c45d19f1bfa1934580b1ba016459675312402"
    # )

    f = open("testdata.xml")

    soup = BeautifulSoup(f, "xml")
    return soup.find_all("item")


# write writes NEW job(s) to json and returns whether it wrote sth
def write(link):
    # Find/open the write destination JSON
    json_data = readfromjson()

    # Check against JSON
    if link not in json_data:

        # Append new links
        json_data.append(link)

        # Re-write to JSON
        writetojson(json_data)

        # Return fact that something is new
        return True

    return False


def readfromjson():
    with open("rsspersist.json") as json_file:
        return json.load(json_file)


def writetojson(towrite):
    with open("rsspersist.json", "w") as json_file:
        json_object = json.dumps(towrite)
        json_file.write(json_object)


main()

# Calls the read method every 60 seconds (maximum allowed frequency)
# schedule.every(60).seconds.do(read)

# while True:  # Don't quite know what this does
#     schedule.run_pending()
#     time.sleep(1)
