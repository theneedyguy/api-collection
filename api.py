#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import json
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} 
req = urllib.request.Request("http://www.gymhofwil.ch/services/mensa", headers=header)
with urllib.request.urlopen(req) as url:  
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
sublinks = soup.find_all("li", class_="sublinks")
link = sublinks[2].a["href"]
dict = {"Mensaplan" : link}
with open("/var/www/api.purpl3.net/hofwil/v1//mensaplan.json", "w") as writeJSON:
    json.dump(dict, writeJSON)
writeJSON.close()
