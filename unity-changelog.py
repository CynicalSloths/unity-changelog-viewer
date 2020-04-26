# import libraries
from src.constants import *
from src.versiondata import *
from src.util import *

import argparse

# Argument parsing
parser = argparse.ArgumentParser(description='Interface for parsing data from the Unity What\'s New website.')
subparsers = parser.add_subparsers(help='sub command interface')
parser.add_argument("-v", help='version')

# Sub Command: list
listParser = subparsers.add_parser("list")
listParser.set_defaults(func=handlerList)
listParser.add_argument("type", default='versions', nargs='?', choices=['versions', 'categories'])
# Sub Command: list
queryParser = subparsers.add_parser("query")
queryParser.set_defaults(func=handlerQuery)
queryParser.add_argument("--range", nargs=2)
queryParser.add_argument("--categories", nargs='*')
queryParser.add_argument("--type", default='all', nargs=1, choices=['all', 'fixes', 'features', 'changes', 'known_issues'])

# parse arguments
args = parser.parse_args()


allVersions = loadUnityVersions()
allVersions.sort(key=lambda x: x.Version)

args.func(args, allVersions)


#import csv
#from datetime import datetime

# open a csv file with append, so old data will not be erased
#with open(‘index.csv’, ‘a’) as csv_file:
# writer = csv.writer(csv_file)
#sss writer.writerow([name, price, datetime.now()])
