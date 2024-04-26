from bs4 import BeautifulSoup
from pymongo import MongoClient

target = "https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml"

client = MongoClient(host="localhost", port=27017)
db = client.crawler
professors = db.professors
pages = db.pages

result = pages.find(filter={"url":target}, projection={"html":1, "_id":0})
html = result[0]["html"]

bs = BeautifulSoup(html, 'html.parser')
names = bs.find("section", {"class":"text-images"}).find_all("h2")
details = bs.find("section", {"class":"text-images"}).find_all("p")

prof_name = []
for name in names:
    prof_name.append(name.get_text())

data = {}
prof_data = []
for item in details:
    temp = item.get_text()
    prof_data.append(temp.split("  "))

for entry in prof_data:
    # Format email
    for i in range(len(entry)):
        if entry[i] == "Email:":
            entry[i] = entry[i] + " " + entry[i+1]
            entry.pop(i+1)
            break 

    # Format web details
    if len(entry) > 5:
        entry[4] = entry[4] + entry[5]
        entry.pop(5)

for i in range(len(prof_data)):
    data_dict = {}
    for item in prof_data[i]:
        values = item.split(":")
        data_dict.update({values[0].lstrip():values[1].lstrip()})
    data.update({prof_name[i].lstrip():data_dict})

for i, j in data.items():
    document = {
        "name":i,
        "title": j.get('Title'),
        "office": j.get('Office'),
        "phone": j.get('Phone'),
        "email": j.get('Email'),
        "website": j.get('Web')
    }
    professors.insert_one(document)
    print("Inserted: " + str(document))