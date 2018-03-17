#!/usr/bin/env python3
from bs4 import BeautifulSoup
import urllib.request
import io, json
articles = { "article": [] }
header = {'User-Agent' : 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19'}
req = urllib.request.Request("https://www.digitec.ch/de/LiveShopping", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
soup = BeautifulSoup(s,"html.parser")
articles = soup.findAll("article")

for article in articles:
	product_content = article.find("div", class_="product-content")
	try:
		product-brand = product_content.find("h5", class_="product-name").find("span", class_="product-brand")
	except:
		pass
	print(product-brand)






#with io.open("/var/www/api.purpl3.net/hofwil/v1/aktuell.json", "w", encoding="utf-8") as writeJSON:
#    writeJSON.write(str(json.dumps(articles, ensure_ascii=True)))
#writeJSON.close()
