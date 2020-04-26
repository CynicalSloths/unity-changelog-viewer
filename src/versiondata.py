import semantic_version
from .constants import *
from .changelog import *
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

class VersionData:
    def __init__(self, url, sem_ver):
        self.URL = url
        self.Version = sem_ver
        self.Changelog = None

    def getChangelog(self):
        if (self.Changelog is None):
            self.Changelog = Changelog(self.URL)
        return self.Changelog

    @classmethod
    def fromHRef(cls, href):
        regexLine = r'[\/aA-zZ\-]+(unity-|)([0-9]+\.[0-9]{1}\.[0-9]{1,2})'
        matchObj = re.match(regexLine, href, re.M|re.I)
        if not matchObj:
            return None
        semVer = semantic_version.Version(matchObj.group(2))
        if (semVer.major < 2017):
            return None
        return cls(UNITY_ROOT + href, semVer)
