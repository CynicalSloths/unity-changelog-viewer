# import libraries
from urllib.request import urlopen
from bs4 import BeautifulSoup
import semantic_version
v = semantic_version.Version('0.1.1')

import re
import constants


class VersionData:
    def __init__(self, url, sem_ver):
        self.URL = url
        self.Version = sem_ver

    @classmethod
    def fromHRef(cls, href):
        regexLine = r'[\/aA-zZ\-]+(unity-|)([0-9]+\.[0-9]{1}\.[0-9]{1})'
        matchObj = re.match(regexLine, href, re.M|re.I)
        if not matchObj:
            return None
        semVer = semantic_version.Version(matchObj.group(2))
        if (semVer.major < 2017):
            return None
        return cls(PAGE_PREFIX + href, semVer)

    def getReleaseNotesBlock(self):
        page = urlopen(self.URL)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')
        mainPage = soup.find('h2', text='Release notes')
        return mainPage.parent

    def getCategories(self):
        mainPage = self.getReleaseNotesBlock()
        cats = mainPage.findAll('h3')
        for cat in cats:
            print(cat)



def findUnityVersions():
    base_search_page = PAGE_PREFIX + 'unity-5.6.0'
    page = urlopen(base_search_page)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    mainPage = soup.find('div', attrs={'class': 'full-release'})
    versionDropdown = mainPage.find('ul', attrs={'class': 'options'})


    entries = versionDropdown.findAll('a')
    versions = []
    for entry in entries:
        hyperlink = entry['href']

        if ('alpha' in hyperlink or 'beta' in hyperlink):
            continue

        versionObj = VersionData.fromHRef(hyperlink)
        if (versionObj is None):
            continue
        versions.append(versionObj)

    for ver in versions:
        ver.getCategories()

    #print(name_box)


def findEntries(website, headerName):
    page = urllib2.urlopen(website)
    # parse the html using beautiful soup and store in variable `soup`
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <div> of name and get its value
    name_box = soup.find('div', attrs={'class': 'full-release'})
    name_box = name_box.find('ul', attrs={'class': 'options'})

    print(name_box)

findUnityVersions()

# specify the url
#quote_page = ‘http://www.bloomberg.com/quote/SPX:IND'
# query the website and return the html to the variable ‘page’
#page = urllib2.urlopen(quote_page)

# parse the html using beautiful soup and store in variable `soup`
#soup = BeautifulSoup(page, ‘html.parser’)

# Take out the <div> of name and get its value
#name_box = soup.find(‘h1’, attrs={‘class’: ‘name’})

#name = name_box.text.strip() # strip() is used to remove starting and trailing
#print name

# get the index price
#price_box = soup.find(‘div’, attrs={‘class’:’price’})
#price = price_box.text
#print price

#import csv
#from datetime import datetime

# open a csv file with append, so old data will not be erased
#with open(‘index.csv’, ‘a’) as csv_file:
# writer = csv.writer(csv_file)
#sss writer.writerow([name, price, datetime.now()])
