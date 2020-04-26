# import libraries
from src.constants import *
from src.versiondata import *
from src.util import *

import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Interface for parsing data from the Unity What\'s New website.')
subparsers = parser.add_subparsers(help='sub command interface')
parser.add_argument("-v", help='version')


listParser = subparsers.add_parser("list")
listParser.add_argument("type", default='versions', nargs='?', choices=['versions', 'categories'])
queryParser = subparsers.add_parser("query")

args = parser.parse_args()

# prepare data
allVersions = loadUnityVersions()
allVersions.sort(key=lambda x: x.Version)



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



#import csv
#from datetime import datetime

# open a csv file with append, so old data will not be erased
#with open(‘index.csv’, ‘a’) as csv_file:
# writer = csv.writer(csv_file)
#sss writer.writerow([name, price, datetime.now()])
