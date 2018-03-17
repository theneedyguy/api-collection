#!/usr/bin/env python3
"""
The API for the Tramdepot seasonal beers.
Version 1.0.1
Author Kevin Christen
"""
from bs4 import BeautifulSoup
import urllib.request
import html
import json
import re
import cgi
from urllib.parse import urljoin
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
req = urllib.request.Request("https://www.altestramdepot.ch/de/unsere-biere", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
# Get each beer element.
div_beers = soup.find_all("div", style="margin-bottom:20px;")
#print(div_beers)
# Loop through each element and substract the last one since it could be non-beer related.
jsonData = {"trambeers": []}
for i in range(0, len(div_beers)):
	beer_descr = ""

	beer_picture = div_beers[i].find("div", class_="span25 padding_left").find("img")["src"]
	beer_picture_joined = urljoin("https://www.altestramdepot.ch/", str(beer_picture).replace(" ", "%20"))

	beer_title = div_beers[i].find("div", class_="span75").find("h3").get_text()
	try:
		beer_description = div_beers[i].find("div", class_="span75").find_all("p")
		for description in beer_description:
			beer_descr+=description.get_text()+"\n"
	except:
		pass
	beer_descr = beer_descr[:-1].replace("\u00a0", "")
	entryJson = {"title" : beer_title,"description": beer_descr, "beer_image" : beer_picture_joined}
	jsonData["trambeers"].append(entryJson)
with open("/var/www/api.purpl3.net/tramdepot/v1/trambeers.json", "w", encoding="utf-8") as writeJSON:
    json.dump(jsonData, writeJSON)
writeJSON.close()
