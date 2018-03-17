#!/usr/bin/env python3
#############################################################################################################################################
#
#
# KUFA API BOT 1.3.2-Stable
# The Kufa API Bot is used to extract data from a website to make it accessible for third parties to develop apps with the data.
# Official URL: https://api.purpl3.net/kufa/v1/events.json
# Update Interval: Daily at 12:00h and 00:00h
# -Changelog 1.3.2
# Added some more badges (isGoes, etc.)
# -Changelog 1.3.1
# Fixes error in mainActDescription
# -Changelog 1.3
# Can now load 'nextevent' events through virtual firefox
# -Changelog 1.2.6-Stable
# Added Listen link for support acts
# Added isMoved badge for events
# -Changelog 1.2.5-Stable
# Added isCancelled for cancelled events
# -Changelog 1.2.4-Stable
# Added Facebook Event Link
# -Changelog 1.2.3-Stable
# Added badge for "SOLD OUT / Ausverkauft"
# Changed User-Agent
# Extracting Country ISO now out of event since it is unecessary data.
# -Changelog 1.2.2-Stable
# Fixed a rare bug with mainActDescription occurring twice when the first Act had a description but the next mainAct had no description.
# -Changelog 1.2.1-Stable
# Added a isSpecial tag for special messages outside of the usual events
# -Changelog 1.2-Stable
# Added a bunch of new badges to the api (isFree, isNew, isExclusive, isTipp, till0530)
# -Changelog 1.1-Stable
# Fixed a bug with eventDescription being newline on some events
# -Changelog 1.0-Stable
# Getting REINHÖREN urls and ticket sale urls now.
# -Changelog 1.0-3Beta
# Using next_siblings in a loop to get consistent data for all main acts and to get rid of excess data in second pass
#
#
#############################################################################################################################################

from bs4 import BeautifulSoup
import urllib.request
import dryscrape
import re
import json
import time

ticketcounter = 0
#urllib for normal webrequest without nextevent
header = {'User-Agent' : 'Kufa API Bot v1.3.1-Stable'} #User Agent is set with some extra info.
req = urllib.request.Request("http://www.kufa.ch", headers=header)
with urllib.request.urlopen(req) as url:
    s = url.read()
#end of urllib request

#dryscrape scraping is only for nextevent tickets because it can handle javascript.
dryscrape.start_xvfb()
session = dryscrape.Session()
session.visit("http://www.kufa.ch")
sesh = session.body()
soup_tickets = BeautifulSoup(sesh,"html.parser")
#end of dryscrape block


#Handles the nexevent tickets and puts them into an array. The array will be counted with ticketcounter
ticket = []
entries_ticket = soup_tickets.find_all("div", { "class" : "ProgEntry" })
for entry in entries_ticket:
    try:
        ticket.append(entry.find("div", {"class": "EventDescription"}).find("span", {"class":"EventSubHeader"}).find("a",href=True)['href'])
    except:
        #ticket = None
        try:
            ticket.append(entry.find("iframe", {"class":"nextevent"})['src'])
        #print(ticket)
        except:
            ticket.append(None)
#End of nextevent handling

soup= BeautifulSoup(s,"html.parser")
entries = soup.find_all("div", { "class" : "ProgEntry" }) #Find every div with class Progentry and save it to variable entries
jsonData = {"events": []} #We need to create a data holder in a JSON format.

SpecialMessage = {"id":0,"eventTitle" : "WERDE MEMBER!", "eventDate": "Unterstütze die Kufa und profitiere dabei!" , "eventDay": "immer", "plus18" : False, "plus20": False, "plus21": False, "plus25": False, "plus30" : False, "freeMember":False, "isNew":False, "isFree":False, "isExclusive":False, "isTipp":False, "till0530":False, "isSpecial":True,"doors": "doors", "images": [], "eventDescription": None, "supportHeader" : None, "supportActs" : [], "mainActs" : [], "ticket": None, "isSoldOut":bool(False), "facebookEvent": None, "isCancelled":bool(False), "isMoved" :bool(False), "isGoes" :bool(False)}
jsonData["events"].append(SpecialMessage)
id = 0 #Initialize ID (Id can be used for sorting)
for entry in entries:
    id = id #Set ID
    isSpecial = False #Set to False because it is only used by Special entries (Default)
    plus18 = False #Set plus18 to False (Default)
    plus20 = False #Set plus20 to False (Default)
    plus21 = False #Set plus21 to False (Default)
    plus25 = False #Set plus25 to False (Default)
    plus30 = False #Set plus30 to False (Default)
    isTipp = False #Set isTipp to False (Default)
    isNew = False #Set  isNew to False (Default)
    isSoldOut = False #Set isSoldOut to False (Default)
    isExclusive = False #Set isExclusive to False (Default)
    till0530 = False #Set till0530 to False (Default)
    isFree = False #Set isFree to False (Default)
    freeMember = False #Set freeMember to False (Default)
    isCancelled = False #Set isCancelled to False (Default)
    isMoved = False # Set isMoved to False (Default)
    isGoes = False # Set isGoes to False (Default)
    facebookEvent = None


    evt = entry.find("div", {"class":"EventDescription"}) #Placeholder evt variable to get all text in EventDescription
    doors = entry.find("div", {"class": "EventDescription"}).find("span", {"class":"EventSubHeader"}).get_text().strip().replace("\n","").replace("  ","") #Get doors before we extract text we dont need
    try:
        facebookEvent = entry.find("a", class_="fbeventlink", href=True)['href'] #Trying to get Facebook Event Links
    except:
        pass # If no Link is present, facebookEvent ist Null
    [ActSubtitle.extract() for ActSubtitle in entry.findAll("span", "ActSubtitle")] #Extracts Country ISO


    mainActs = [] #Initializes our empty mainActs array
    for x in entry.find("div", {"class": "EventDescription"}).findAll("h2"): #Get all h2 which contain the name of the main act
        mainActName = x.get_text() #This one is easy since it is the text of h2
        mainActGenre = x.next_sibling.strip() #This one follows the h2 and should most of the time be the genre of the act
        mainActImage = "".join([img["src"] for img in x.next_sibling.next_sibling.findAll("img")]) #This get the image of every main act. Sets "" of no image found.
        siblings = []
        mainActDescription = None
        mainActWebsite = ""
        mainActListen = ""
        for sibling in x.next_siblings: #Get all siblings after h2
            if str(sibling).startswith("<b><a"):
                actURLS = [x["href"] for x in sibling.findAll("a")] #Get all links after h2
                mainActWebsite = actURLS[0] #0 is usually the website of act
                try:
                    mainActListen = actURLS[1] #1 is the REINHOEREN url of act
                except:
                    mainActListen = None
                pass
            elif str(sibling).startswith("<p><strong>"): #Coupe Romanoff stuff we dont need
                pass
            elif str(sibling).startswith("<p>"): #Get all p after h2
                mainActDescription = None
                siblings.append(sibling.get_text()) #Append each sibling to siblings array
                mainActDescription = "\n".join(siblings) #Join array to make it a text again
        #print(siblings)
        if mainActWebsite == "":
            mainActWebsite = None
        if mainActListen == "":
            mainActListen == None
        if (mainActDescription == "") or (mainActDescription == "\n"):
            mainActDescription = None
        if mainActGenre.strip() == "":
            mainActGenre = None
        if mainActImage == "":
            mainActImage = None
        mainActs.append({"name" : mainActName,"website" : mainActWebsite, "listen": mainActListen,"description": mainActDescription, "genre" : mainActGenre, "image" : mainActImage})
    supportActs = [] #Initialze empty SupportActs array
    for x in entry.find("div", {"class": "EventDescription"}).findAll("span", {"class":"SupportActTitle"}): #Get text inside SupportActTitle
        supportActName = x.get_text() #Get SupportAct name
        supportActWebsite = "".join([a["href"] for a in x.findAll("a",href=True)]) #Get website of supporting Act
        if supportActWebsite == "": #If no website found set null
            supportActWebsite = None
        supportActGenre = x.next_sibling #Get SupportAct genre

        supportActMusic = None
        supportActListen = x.next_sibling.next_sibling
        if not str(supportActListen).startswith("<br/>") or str(supportActListen == None):
            try:
                supportActLink = re.findall('"([^"]*)"'  ,str(supportActListen))
                supportActMusic = supportActLink[0]
            except:
                pass
        else:
            supportActMusic = None

        supportActs.append({"name" : supportActName, "genre" : supportActGenre, "website": supportActWebsite, "listen": supportActMusic}) #Append to SupportAct Array
    for span in evt("span","SupportActTitle"): #Extract text following the SupportActs
        span.next_sibling.extract()
    for span in evt("span","SupportActTitle"): #Extract SupportActTitle since we have them saved in an array
        span.extract()
    for div in evt("div","labels"): #Extract labels (bottom of ProgEntry)
        div.extract()
    for span in evt("span", "EventSubHeader"): #Extract doors time
        span.extract()
    for h2 in evt("h2"): #This part gets rid of all excess information we already have in our mainActs Array
        h2.next_sibling.extract() #Get rid of genres first
        for rmSibling in h2.next_siblings:
            if str(rmSibling).startswith("<b><a"): #delete all links
                rmSibling.extract()
            elif str(rmSibling).startswith("<p>"): #delete all text
                for sib in rmSibling:
                    sib.extract()
            else:
                h2.extract() #Delete h2 in the end
    evet = re.sub("()expander_hide\('#Details\d{4}()'\)();", '', evt.get_text()) #Extract unecessary html and save it to placeholder variable "evet"
    eventDescription = evet.strip().replace("WEBSEITE / REINHÖREN","").replace("WEBSEITE", "").replace("SUPPORT:","").replace("REINHÖREN","").replace("\n\n","\n").replace("  ","") #Put data in eventDescription variable
    if eventDescription == "\n\n\n":
        eventDescription = None
    elif eventDescription == "":
        eventDescription = None
    elif eventDescription == "\n":
        eventDescription = None

    #Get ProgButtons to determine minimum age and fee for members.
    progButtons = [x["src"] for x in entry.findAll("img", {"class": "ProgButton"})]
    for btn in progButtons:
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/18.png":
            plus18 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/20.png":
            plus20 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/21.png":
            plus21 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/25.png":
            plus25 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/30.png":
            plus30 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/member-gratis.png":
            freeMember = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/tipp.png":
            isTipp = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/gratis.png":
            isFree = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/bis0530.png":
            till0530 = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/exklusiv.png":
            isExclusive = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/neu.png":
            isNew = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/ausverkauft.png":
            isSoldOut = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/abgesagt.png":
            isCancelled = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/verschoben.png":
            isMoved = True
        if btn == "http://www.kufa.ch/wp-content/themes/oxygen-child/images/kufagoes.png":
            isGoes = True
    #End of determining age and member fee

    eventTitle = entry.find("a", {"class": "EventDetails"}).get_text().strip().replace("\t","").replace("\n\n","\n") #Get eventTitle
    eventImg = [x["src"] for x in entry.findAll("img", {"class": "attachment-full"})] #Get all Act Images
    supportHeader = "SUPPORT:" #Set support header. Not necessarily needed.
    eventDate = entry.find("span", {"class": "EventDate"}).get_text().strip().replace("\t","").replace("\n\n","\n").replace("  ","") #Get event date
    eventDay = entry.find("span", {"class": "EventDay"}).get_text().strip().replace("\t","").replace("  ","").replace("\n","") #Get day of event
    entryJson = {"id": int(id), "eventTitle" : eventTitle, "eventDate": eventDate , "eventDay": eventDay, "plus18" : bool(plus18), "plus20": bool(plus20), "plus21": bool(plus21), "plus25": bool(plus25), "plus30" : bool(plus30), "freeMember":bool(freeMember), "isNew":bool(isNew), "isFree":bool(isFree), "isExclusive":bool(isExclusive), "isTipp":bool(isTipp), "till0530":bool(till0530), "isSpecial":bool(isSpecial), "isSoldOut":bool(isSoldOut)  ,"doors": doors, "images": eventImg, "eventDescription": eventDescription, "supportHeader" : supportHeader, "supportActs" : supportActs, "mainActs" : mainActs, "ticket": ticket[ticketcounter], "facebookEvent":facebookEvent, "isCancelled":bool(isCancelled), "isMoved":bool(isMoved), "isGoes":bool(isGoes)} #put it in JSON
    jsonData['events'].append(entryJson) #Append JSON to the jsonData variable at Key "events"
    id += 1 #Count ID up.
    ticketcounter += 1
with open("/var/www/api.purpl3.net/kufa/v1/events.json", "w", encoding="utf-8") as writeJSON:
    json.dump(jsonData, writeJSON, indent=4, sort_keys=True)
writeJSON.close()
