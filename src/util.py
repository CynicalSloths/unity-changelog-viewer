from .constants import *
from .versiondata import *

from urllib.request import urlopen
from bs4 import BeautifulSoup

def loadUnityVersions():
    base_search_page = PAGE_PREFIX_PATH + '/unity-5.6.0'
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
    return versions
