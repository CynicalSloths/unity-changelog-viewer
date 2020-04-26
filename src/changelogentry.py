import re

class ChangelogEntry:
    def __init__(self, category, change, issueReferences = None):
        self.Category = category
        self.Value = change
        if issueReferences is None:
            self.Issues = []
        else:
            self.Issues = issueReferences

    def getValue(self):
        return self.Value

    def getCategory(self):
        return self.Category

    def getIssues(self):
        return self.Issues

    @classmethod
    def fromParagraph(cls, paragraph):
        paragraph = paragraph.replace("\n", "")
        regexLine = r'\(([0-9\,]+)\)$'
        fixVersionStrings = re.findall(regexLine, paragraph)
        fixVersions = []
        if len(fixVersionStrings) > 0:
            for entry in fixVersionStrings[0].split(","):
                fixVersions.append(int(entry.strip()))
        paragraph = paragraph.replace('({0})'.format(fixVersionStrings), '')

        matchObj = re.match(r'([aA-zZ0-9\-\ ]+){1}\:(.*)', paragraph)
        if matchObj is None:
            return None
        return cls(matchObj.group(1).strip(), matchObj.group(2).strip(), fixVersions)

        #semVer = semantic_version.Version(matchObj.group(2))
        #print(paragraph)
