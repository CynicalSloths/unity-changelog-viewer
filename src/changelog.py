from .changelogentry import *
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

class Changelog:
    def __init__(self, url):
        self.KnownIssues = None
        self.Fixes = None
        self.Improvements = None
        self.Features = None
        self.APIChanges = None
        self.Changes = None

        page = urlopen(url)
        # parse the html using beautiful soup and store in variable `soup`
        soup = BeautifulSoup(page, 'html.parser')
        mainPage = soup.find('h2', text='Release Notes')
        self.PageData = mainPage.parent.find('div', attrs={'class': 'release-notes'})



    #Loadall
    def loadAll(self):
        self.getKnownIssues()
        self.getFixes()
        self.getImprovements()
        self.getFeatures()
        self.getAPIChanges()
        self.getChanges()
        
    def getEntries(self, type):
        if type == 'all' or type == 'known_issues':
            for issue in self.getKnownIssues():
                yield issue
        if type == 'all' or type == 'fixes':
            for fix in self.getFixes():
                yield fix
        if type == 'all' or type == 'features':
            for improvement in self.getImprovements():
                yield improvement
        if type == 'all' or type == 'features':
            for feature in self.getFeatures():
                yield feature
        if type == 'all' or type == 'changes':
            for change in self.getAPIChanges():
                yield change
        if type == 'all' or type == 'changes':
            for change in self.getChanges():
                yield change

    def getAllEntryCategories(self):
        self.loadAll()
        categories = []
        if (self.KnownIssues is not None):
            for issue in self.KnownIssues:
                categories.append(issue.getCategory())

        if (self.Fixes is not None):
            for fix in self.Fixes:
                categories.append(fix.getCategory())

        if (self.Improvements is not None):
            for improvement in self.Improvements:
                categories.append(improvement.getCategory())


        if (self.Features is not None):
            for feature in self.Features:
                categories.append(feature.getCategory())


        if (self.APIChanges is not None):
            for change in self.APIChanges:
                categories.append(change.getCategory())


        if (self.Changes is not None):
            for change in self.Changes:
                categories.append(change.getCategory())
        return list(set(categories))

    # Known issues
    def getKnownIssues(self):
        if (self.KnownIssues is not None):
            return self.KnownIssues
        self.KnownIssues = []
        for entry in self.getChangelogEntry('known issues', 'h3'):
            self.KnownIssues.append(entry)
        return self.KnownIssues

    # changelog
    def getFixes(self):
        if (self.Fixes is not None):
            return self.Fixes
        self.Fixes = []
        for entry in self.getChangelogEntry('fixes'):
            self.Fixes.append(entry)
        return self.Fixes

    def getImprovements(self):
        if (self.Improvements is not None):
            return self.Improvements
        self.Improvements = []
        for entry in self.getChangelogEntry('improvements'):
            self.Improvements.append(entry)
        return self.Improvements

    def getFeatures(self):
        if (self.Features is not None):
            return self.Features
        self.Features = []
        for entry in self.getChangelogEntry('features'):
            self.Features.append(entry)
        return self.Features

    def getAPIChanges(self):
        if (self.APIChanges is not None):
            return self.APIChanges
        self.APIChanges = []
        for entry in self.getChangelogEntry('api changes'):
            self.APIChanges.append(entry)
        return self.APIChanges

    def getChanges(self):
        if (self.Changes is not None):
            return self.Changes
        self.Changes = []
        for entry in self.getChangelogEntry('changes'):
            self.Changes.append(entry)
        return self.Changes

    # helpers
    def getChangelogEntry(self, keyword, elementType = 'h4'):
        for entry in self.iterateElements(elementType, keyword.lower()):
            changelogEntry = ChangelogEntry.fromParagraph(entry.text.strip())
            if changelogEntry is None:
                print ("Error: entry {0} could not be parsed.".format(entry.text.strip()))
                continue
            yield changelogEntry


    def iterateElements(self, elementType, startElementSearchString):
        inside = False
        additional = None
        for entry in self.PageData:
            if entry is None:
                continue
            if entry.name is None:
                continue
            if entry.name == elementType:
                if startElementSearchString in entry.text.lower():
                    inside = True
                    continue
                elif inside:
                        inside = False
                        break

            if inside and entry.name == 'ul':
                additional = entry.findAll('li')
                break
            elif inside:
                if ':' in entry.text.lower():
                    yield entry
        if additional is not None:
            for entry in additional:
                if entry is None or not ':' in entry.text.lower():
                    continue
                yield entry
