# Ali express product import
import csv
import sys
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
        # Gets URL to description & urls of pictures in slider
        descurl, slidepics = scrape.getDescNSlidePics(soup)
        descsource = selsource.getSource(descurl)
        descsoup = scrape.getSoup(descsource)
        descpics = scrape.getDescPics(descsoup)
        proddir, slidedir = scrape.makeProdDirs(rootpath, dirname)
        filemap.append((title, proddir))
        scrape.fetchPics(dirname, slidedir, slidepics)
        scrape.fetchPics(dirname, proddir, descpics)
    except:
        pass

selsource.quitSession()
csvname = '/'.join([rootpath, 'filemap.csv'])
with open(csvname, 'w', newline='') as file:
    writer = csv.writer(file)
    for item in filemap:
        try:
            writer.writerow(item)
        except:
            pass
