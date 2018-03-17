#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import json
import datetime
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'} 
req = urllib.request.Request("http://www.hydrodaten.admin.ch/de/2135.html", headers=header)
with urllib.request.urlopen(req) as url:  
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
sublinks = soup.find_all("td", class_="text-center")
dict = {"aaretemp_last" : float(sublinks[2].get_text()), "abfluss_last" : float(sublinks[0].get_text()), "aaretemp_mid24" : float(sublinks[5].get_text()) , "abfluss_mid24" : float(sublinks[3].get_text()), "abfluss_max24" : float(sublinks[6].get_text()), "aaretemp_max24" : float(sublinks[8].get_text()), "time" : str(datetime.datetime.now())}
with open("/var/www/api.purpl3.net/aare/v1/aare.json", "w") as writeJSON:
    json.dump(dict, writeJSON)
writeJSON.close()
