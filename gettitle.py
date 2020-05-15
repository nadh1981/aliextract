# Ali express product import
# from bs4 import BeautifulSoup as bs

import re
import os
import time
import inspect
import json
import sys
import shutil
import csv

from myaliextract import selsource
from myaliextract import scrape

listfile = sys.argv[1]
rootdir = sys.argv[1].split('/')
rootdir.pop()
rootpath = '/'.join(rootdir)
linklist = open(listfile, "r")
products = []
filemap = []

for link in linklist:
	dirname = link.split('/').pop()
	dirname = dirname.split('.')[0]
	source = selsource.getSource(link)
	soup = scrape.getSoup(source)
	try:
		title = scrape.getTitle(soup)
		proddir = '/'.join([rootpath,dirname])
		filemap.append((title, proddir))
	except:
		pass

selsource.quitSession()

print(filemap)

csvname = '/'.join([rootpath,'filemap.csv'])

with open(csvname, 'w', newline='') as file:
	writer = csv.writer(file)
	for item in filemap:
		try:
			writer.writerow(item)
		except:	
			pass