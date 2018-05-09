#!/usr/bin/env python3

"""
The API for Denner aktionen.
Version: 1.0
Author: Kevin Christen
"""

from bs4 import BeautifulSoup
from bs4.element import Tag
import urllib.request
import html
import json
import re
from urllib.parse import urljoin
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
req = urllib.request.Request("https://www.denner.ch/de/aktionen/", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
soup = BeautifulSoup(s,"html.parser")

# Get each element of the sales
div_aktionen = soup.select("div.carosel-item.article-item")

# Define empty dictionary
jsonData = {"aktionen": []}

# Define the base URL to concat the links to
base_URL = "https://www.denner.ch/"


for aktion in div_aktionen:
	# Get title
	title = aktion.find("h3", class_="listh3").get_text()
	# Get description
	description = aktion.find("span", class_="beschreibung").get_text()
	# Get link
	link = aktion.find("a", class_="no-padding", href=True).attrs['href']
	# Get reduced price
	try:
		# Remove nested item
		reduced = aktion.find("span", class_="aktuell")
		reduced.find("span", class_="small").extract()
	except:
		pass
	# Create the dictionary
	entryJson = {"title" : title, "reduced_price" : reduced.get_text(strip=True), "description" : description, "link": base_URL+link}
	# Append it to the json
	jsonData["aktionen"].append(entryJson)

with open("/var/www/api.purpl3.net/aktionen/v1/denner.json", "w", encoding="utf-8") as writeJSON:
    json.dump(jsonData, writeJSON, indent=4, sort_keys=True)
writeJSON.close()


