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

def filterRange(allVersions, startVersion, endVersion):
    list = []
    for versionObj in allVersions:
        semVer = versionObj.getVersion()
        if startVersion > semVer or endVersion < semVer:
            continue
        list.append(versionObj)
    return list

def handlerList(args, allVersions):
    if 'type' in vars(args):
        if args.type == 'versions':
            print ('Version releases of Unity3D since 2017:')
            for version in allVersions:
                print (version.Version)
        elif args.type == 'categories':
            print("Categories contained in the last 10 releases:")
            categories = []
            for version in allVersions[-10:]:
                for entry in version.getChangelog().getAllEntryCategories():
                    categories.append(entry)
            categories = list(set(categories))
            categories.sort()
            for cat in categories:
                print(cat)

def getIssues(versions, type, categoryFilter):
    resultSet = []
    for versionObj in versions:
        changelogInfo = versionObj.getChangelog()
        for entry in changelogInfo.getEntries(type):
            if categoryFilter is not None and len(categoryFilter) > 0 and not entry.getCategory() in categoryFilter:
                continue
            resultSet.append('{0}: {1}'.format(entry.getCategory(), entry.getValue()))
    resultSet = list(set(resultSet))
    resultSet.sort()
    return resultSet

def handlerQuery(args, allVersions):
    if 'range' in vars(args) and args.range is not None and len(args.range) > 0:
        if not (VersionData.isVersionString(args.range[0]) and VersionData.isVersionString(args.range[1])):
            print ('Invalid version passed into --range: {0}. Support is only provided for Unity3D versions 2017 and up (e.g. 2019.1.1).'.format(args.range))
            exit()
        startVersion = semantic_version.Version(args.range[0])
        endVersion = semantic_version.Version(args.range[1])

        if endVersion < startVersion:
            buffer = endVersion
            endVersion = startVersion
            startVersion = buffer
        allVersions = filterRange(allVersions, startVersion, endVersion)
    queryType = args.type
    if queryType is None:
        queryType = 'all'
    else:
        queryType = queryType[0]
    for entry in getIssues(allVersions, queryType, args.categories):
        print (entry)
