#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from threading import Thread
from datetime import datetime
from configparser import ConfigParser

# ---------------------------------- #
# --------- Configurations --------- #
# ---------------------------------- #
matches = ["http://", "https://"]
LastVulnValue = []

# --------------------------------- #
# ------------ Helpers ------------ #
# --------------------------------- #

def GetConfigurations(get):
    # instantiate
    config = ConfigParser()

    # parse existing file
    config.read('config.ini')

    # read values from a section
    if get == "Interval":
        return config.getint('Service', 'Interval')
    elif get == "DatabasePath":
        return config.get('DatabaseConfigurations', 'DatabasePath')

def Monitor(Severity, Description, Value):
    print(Severity, str(GetToday()), Description, Value)

def GetToday():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def Request(URL):
    return requests.get(URL)

def GetLastVulnValue():
    try:
        LastVulnValue.append(sqlite3.connect(GetConfigurations('DatabasePath')).cursor().execute("SELECT VULNID FROM Vuln ORDER BY VULNID DESC LIMIT 1").fetchone()[0] + 1)
    except Exception as Error:
        Monitor("Error", str(Error), "")

def CheckDataIsExist(ID, DatabaseName, Value):
    try:
        if sqlite3.connect(GetConfigurations('DatabasePath')).cursor().execute("SELECT "+str(ID)+" FROM "+DatabaseName+" WHERE "+str(ID)+" = ?", (Value,)).fetchone() is None:
            return False
        else:
            return True

    except Exception as Error:
        Monitor("Error", str(Error), "")

# --------------------------------- #
# ----------- Inserters ----------- #
# --------------------------------- #

def InsertPhishData(PHISHID, URL, DESCRIPTION, SOURCE, DATE):

    try:
        if CheckDataIsExist("PHISHID", "Phish",PHISHID) == False:
            Connection = sqlite3.connect(GetConfigurations('DatabasePath'))
            Cursor = Connection.cursor()
            Cursor.execute("INSERT INTO Phish (PHISHID, URL, DESCRIPTION, SOURCE, DATE) VALUES (?,?,?,?,?)", (PHISHID,URL,DESCRIPTION,SOURCE,DATE))
            Connection.commit()
            Cursor.close()
            Monitor("Info", "Malicious link has been inserted to database successfully", URL)

    except Exception as Error:
        Monitor("Error", str(Error), "")

def InsertSecurityAnnouncementData(VULNID,DESCRIPTION,VULNTITLE,DATE):

    try:
        if CheckDataIsExist("VULNID", "Vuln", VULNID) == False:
            Connection = sqlite3.connect(GetConfigurations('DatabasePath'))
            Cursor = Connection.cursor()
            Cursor.execute("INSERT INTO Vuln (VULNID,DESCRIPTION, VULNTITLE, DATE) VALUES (?,?,?,?)", (VULNID, DESCRIPTION,VULNTITLE,DATE))
            Connection.commit()
            Monitor("Info", "Security announcement has been inserted to database successfully", VULNTITLE)

    except Exception as Error:
        Monitor("Error", str(Error), "")

# --------------------------------- #
# ---------- Collectors ----------- #
# --------------------------------- #

def CollectSecurityAnnouncement():
    Monitor("Info", "Security announcement ckecking now, please wait.", "")

    while True:
        try:
            Response = BeautifulSoup(Request('https://www.usom.gov.tr/tehdit/'+str(LastVulnValue[0] + 1)+'.html').content,"lxml")
            if "not found" not in Response.text:
                Vulntitle = Response.find('h1').text
                Description = Response.find("div", {"class":"article"}).text.replace(Vulntitle,"")
                Date = GetToday()
                        
                if CheckDataIsExist("VULNID", "Vuln", LastVulnValue[0]) == False:    
                    InsertSecurityAnnouncementData(LastVulnValue[0], Description, Vulntitle, Date)
                else:
                    LastVulnValue[0] = LastVulnValue[0] + 1
            else:
                pass

        except Exception as Error:
            LastVulnValue[0] = LastVulnValue[0] + 1
            Monitor("Error", str(Error),"")
        
        time.sleep(GetConfigurations('Interval'))
    

def CollectPhishLinks():
    Monitor("Info", "Phishing links ckecking now, please wait.", "")
    while True:

        try:
            Response = BeautifulSoup(Request('https://www.usom.gov.tr/zararli-baglantilar/1.html').content,"lxml")
            Tables = Response.find("table")
            Fields = Response.findAll('td')

            for i in range(0, len(Fields), 5):
                InsertPhishData(Fields[i].text, 
                                Fields[i + 1].text,
                                Fields[i + 2].text,
                                Fields[i + 3].text, 
                                GetToday())

        except Exception as Error:
            Monitor("Error", str(Error), Fields[i + 1].text)
                    
        time.sleep(GetConfigurations('Interval'))

# --------------------------------- #
# ------------ Threads ------------ #
# --------------------------------- #

if __name__ == "__main__":
    GetLastVulnValue()

    CollectSecurityAnnouncement = Thread(target = CollectSecurityAnnouncement)
    CollectPhishLinks = Thread(target = CollectPhishLinks)

    CollectSecurityAnnouncement.start()
    CollectPhishLinks.start()
