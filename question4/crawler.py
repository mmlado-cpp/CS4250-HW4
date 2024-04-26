from urllib.request import urlopen
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re

frontier = []
visited = []
frontier.append("https://www.cpp.edu/sci/computer-science/")


# Set up database connection, create database and collection
client = MongoClient(host="localhost", port=27017)
db = client.crawler
pages = db.pages

def crawlerThread(frontier):
    counter = 0
    while len(frontier) != 0:
        url = frontier.pop(0)
        visited.append(url)
       
        html = urlopen(url)
        html = html.read()
        
        data = html.decode(encoding="iso-8859-1")
        document = {
            "url":url,
            "html":data
        }
        pages.insert_one(document)

        bs = BeautifulSoup(html, 'html.parser')
        if bs.find("h1", string="Permanent Faculty"):
            frontier.clear()
            print("Found (attempts:"+ str(counter) + ")")
        else:
            counter = counter +1
            print("Not found")
            for link in bs.find_all("a", href=True):
                temp = link['href']

                # Fix relative links before adding to frontier
                if (re.match("^https://www.cpp.edu", temp) == None):
                    temp = "https://www.cpp.edu" + temp

                if temp not in visited:
                    frontier.append(temp)

crawlerThread(frontier)