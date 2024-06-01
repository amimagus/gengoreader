import json
import os
import smtplib
import socket
import time

import requests
import schedule
from bs4 import BeautifulSoup

HOST = "0.0.0.0"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)

# Clear rsspersist json as first action
with open("rsspersist.json", "r") as r:
    data = json.load(r)
    data = []
    with open("rsspersist.json", "w") as w:
        data = json.dump(data, w)


# main is the driver method. It calls the read and write functions and notifies the user of new jobs.
def main():

    newjobs = []
    comparisoncounter = 0
    items = read()
    for item in items:
        link = item.link.text

        # If return value of write is True, add to list and send an email of that list. If false, do nothing.
        if write(link):
            newjobs.append(link)
            comparisoncounter += 1

    if comparisoncounter != 0:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            email = os.getenv("EMAIL")
            password = os.getenv("PASSWORD")
            subject = "New jobs"
            text = f"Subject: {subject}\n\n{newjobs}"
            server.starttls()
            server.login(email, password)
            server.sendmail(email, email, text)
            server.quit()
        except Exception as e:
            print(f"An error occurred: {str(e)}")


# read gets all available jobs and sanitizes them
def read():
    url = requests.get(
        "https://gengo.com/rss/available_jobs/57c56531c6ec0e741c45d19f1bfa1934580b1ba016459675312402"
    )

    # # This line is to test with dummy data. When there's a live job, use url.content in place of f.
    # f = open("testdata.xml")

    soup = BeautifulSoup(url.content, "xml")
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


# Calls the main method every 60 seconds (maximum allowed frequency)
schedule.every(60).seconds.do(main)

# Don't quite know what this does
while True:
    schedule.run_pending()
    time.sleep(1)
