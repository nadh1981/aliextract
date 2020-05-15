import re
import json
import os
import shutil
import time
import urllib.request
from bs4 import BeautifulSoup as bs


def getSoup(source):
    return bs(source, 'html.parser')


def getTitle(soup):
    title = soup.findAll('div', attrs={'class': 'product-title'})[0].getText()
    return title


def makejson(soup):
    pattern = re.compile(r'window.runParams.*')
    script = soup.findAll('script', text=pattern)
    script_str = script[0].text
    json_str = script_str[str(script_str).find('window.runParams = {'):str(script_str).find('var GaData')].replace(
        'window.runParams = ', '').replace('var GaData', '').strip().replace('data', '"data"').replace("};", "}")
    json_str = re.sub('}},(?=\n)((?:\n.+)+)', '}}}', json_str).strip()
    json_data = json.loads(json_str)
    return json_data


def getDescNSlidePics(soup):
    slidepics = []
    json_data = makejson(soup)
    descUrl = json_data['data']['descriptionModule']['descriptionUrl']
    prodSKUPropList = json_data['data']['skuModule']['productSKUPropertyList']
    # get pics for variants
    for prodSKUPropItem in prodSKUPropList:
        skuPropValues = prodSKUPropItem['skuPropertyValues']
        for skuPropValue in skuPropValues:
            try:
                slidepics.append(skuPropValue['skuPropertyImagePath'])
            except:
                pass
    # get pics that are not variants
    slidediv = soup.find('ul', attrs={'class': 'images-view-list'})
    slidethumbs = slidediv.findAll('img')
    for thumb in slidethumbs:
        img = thumb['src']
        img = img.replace('jpg_50x50.', '')
        slidepics.append(img)
    return [descUrl, slidepics]


def getDescPics(soup):
    desc_pics = []
    descImages = soup.findAll('img')
    for img in descImages:
        try:
            desc_pics.append(img['src'])
        except:
            pass
    return desc_pics


def makeProdDirs(rootdir, dirname):
    proddir = '/'.join([rootdir, dirname])
    if os.path.exists(proddir):
        shutil.rmtree(proddir)
    os.mkdir(proddir)
    slidedir = '/'.join([proddir, 'slides'])
    os.mkdir(slidedir)
    return [proddir, slidedir]


def fetchPics(dirname, folder, pics):
    print(pics)
    for index, pic in enumerate(pics):
        if 'https' not in pic:
            pic = 'https:' + pic
        picname = getPicName(index + 1, dirname, folder, pic)
        print(pic, picname)
        urllib.request.urlretrieve(pic, picname)
        time.sleep(int(10))


def getPicName(index, dirname, folder, pic):
    pictype = pic.split('.').pop()
    picname = '-'.join([dirname, str(index)])
    picname = '.'.join([picname, pictype])
    return '/'.join([folder, picname])
