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
from urllib.parse import urljoin
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
req = urllib.request.Request("https://www.altestramdepot.ch/de/home", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
# Get each news element.
div_news = soup.find_all("div", class_="collapse")
# Loop through each element and substract the last one since it could be non-beer related.
jsonData = {"beers": []}
for i in range(0, len(div_news)):
    try:
        #Get name of beer
        titel_h2 = div_news[i].find("div", class_="titel").find("h2").get_text()
        #Get beer details
        news_info_h3 = div_news[i].find("div", class_="titel").find("h3").get_text()
        #Get Litres left
        news_info_fuellstand_stand_h3 = div_news[i].find("div", class_="titel").find("div", class_="bierstand").find("h3").get_text()
        #Get image URL, and join it with normal URL.
        news_info_fuellstand_img_src = div_news[i].find("div", class_="titel").find("div", class_="bierstand").find("div", class_="tank").find("img")["src"]
        news_info_fuellstand_img_src_joined = urljoin("https://www.altestramdepot.ch/de/home", news_info_fuellstand_img_src)
        #Get beer description and remove all breaks and p and replace breaks with newline char. And unescape results for proper text.
        news_info_description_p = div_news[i].find("div", class_="antwort").find("div", class_="antwortinhalt").find("p")
        news_info_description_all_p = div_news[i].find("div", class_="antwort").find("div", class_="antwortinhalt").findAll("p")
        news_info_description_p_string = ""
        for p in news_info_description_all_p:
            news_info_description_p_string += str(p).replace("<p>", "").replace("<br/>", "\n").replace("</p>", "")


        #news_info_description_p_string = str(news_info_description_p).replace("<p>", "").replace("<br/>", "\n").replace("</p>", "")
            news_info_description_p_string_unescape = html.unescape(news_info_description_p_string)

        #Fill values into string.
        entryJson = {"title" : titel_h2, "details" : news_info_h3, "litres_left" : news_info_fuellstand_stand_h3, "description": news_info_description_p_string_unescape, "litres_image" : news_info_fuellstand_img_src_joined}
        #Check if not a beer. If beer, append to jsonData, else pass.
        if div_news[i].find("div", class_="titel").find("div", class_="bierstand") != None:
            jsonData["beers"].append(entryJson)
    except:
        pass
with open("/var/www/api.purpl3.net/tramdepot/v1/beers.json", "w", encoding="utf-8") as writeJSON:
    json.dump(jsonData, writeJSON)
writeJSON.close()
