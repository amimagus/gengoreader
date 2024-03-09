import json
import smtplib

# import schedule
from bs4 import BeautifulSoup

# import requests
# from plyer import notification
# import time


# main is the driver method. It calls the read and write functions and notifies the user of new jobs.
def main():

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
    server = smtplib.SMTP("smtp.gmail.com", 587)
    send = input("SENDER EMAIL: ")
    receive = input("RECEIVER EMAIL: ")
    server.starttls()
    server.login(input("EMAIL: "), input("PASSWORD: "))
    subject = "New jobs"
    text = f"Subject: {subject}\n\n{newjobs}"
    server.sendmail(send, receive, text)
    # notification.notify(
    #     title="NEW JOB!",
    #     message=f"{newjobs}",
    #     app_icon=None,
    #     timeout=10,
    # )

    # print("END OF AVAILABLE JOBS\n")


# read gets all available jobs and sanitizes them
def read():
    # url = requests.get(
    #     "https://gengo.com/rss/available_jobs/57c56531c6ec0e741c45d19f1bfa1934580b1ba016459675312402"
    # )

    # This line is to test with dummy data. When there's a live job, use url.content in place of f.
    f = open("testdata.xml")

    soup = BeautifulSoup(f, "xml")
    return soup.find_all("item")


# write writes NEW job(s) to json and returns whether it wrote sth
def write(link):
    # Find/open the write destination JSON
    json_data = readfromjson()

    # Check fetched jobs against JSON
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
