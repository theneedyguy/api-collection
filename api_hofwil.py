#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import io, json
from collections import defaultdict
articles = defaultdict(list)
header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) - HofwilApp API Bot v1.1'}
req = urllib.request.Request("http://www.gymhofwil.ch/aktuell/vorschau", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
left = soup.find_all("div", class_="left")
row = soup.findAll("div", class_="row")
middle = soup.find_all("div", class_="middle")
articles["news"].append(("Hofwilapp Update","Bis auf weiteres werden für die HofwilApp nur noch Maintenance Updates erscheinen, um die Daten aktuell zu halten."))


for elm in row:
	descr=""
	left = elm.find("div", class_="left")
	middle = elm.find("div", class_="middle")

#	titles = middle.findAll("strong")
#	for title in titles:
#		title.extract()
	title_aktuelles=left.get_text()
	titles = middle.findAll("strong")
	for title in titles:
		if len(title.get_text()) != 0:
			#title_aktuelles = title.get_text()
			pass
		else:
			title.extract()
		for sibling in title.next_siblings:
			if not str(sibling).startswith("<") and not str(sibling).startswith(" (pdf"):
				descr += str(sibling)+"\n"

	#print(middle)
#for element in middle:
#	descr = ""
#	titles = element.findAll("strong")
#	for title in titles:
#		if len(title.get_text()) != 0:
#			title_aktuelles = title.get_text()
#		else:
#			title.extract()
#		for sibling in title.next_siblings:
#			if not str(sibling).startswith("<") and not str(sibling).startswith(" (pdf"):
#				descr += str(sibling)+"\n"
	articles["news"].append((title_aktuelles, descr))
with io.open("/var/www/api.purpl3.net/hofwil/v1/aktuell.json", "w", encoding="utf-8") as writeJSON:
    writeJSON.write(str(json.dumps(articles, ensure_ascii=True)))
writeJSON.close()
