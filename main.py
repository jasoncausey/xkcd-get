# Multi-threaded python program to download xkcd comics, along with the heading and the alt-text.
__author__ = 'TheUbermanIsHere'

import re
import os
import requests
import bs4
from PIL import Image,ImageDraw,ImageFont
import textwrap

pngReg = re.compile(r'[a-zA-Z0-9]*.(png|jpg)')
dirdump = os.listdir()

for i in reversed(dirdump):
    b = pngReg.search(i)
    if b is None:
        dirdump.remove(i)

dirdump = sorted(dirdump)
dirlist = list()

for i in dirdump:
    i = i.split('.')
    i = i[0]
    dirlist.append(int(i))

print(dirlist)

home = requests.get('http://xkcd.com')
home.raise_for_status()
bs = bs4.BeautifulSoup(home.text,"lxml")

text = bs.select('#middleContainer')
textRe = re.compile(r'http.*\.png')
aa = textRe.search(text[0].getText())

initRe = re.compile(r'http://xk.*/')
b = initRe.search(text[0].getText())

bRe = re.compile(r'\d\d\d\d')
bb = bRe.search(b.group())

counter = int(bb.group())

# Create a list of all the comics to be downloaded.

downlist = list(i for i in range(1,counter))
downlist = list(set(downlist) - set(dirlist))

def xkcd(a):
    for i in a:
        print("Currently downloading comic: " + str(i))
        page = requests.get('http://xkcd.com/' + str(i))
        page.raise_for_status()
        bs = bs4.BeautifulSoup(page.text,"lxml")
        title = bs.select('#ctitle')
        title = title[0].getText()
        print(title)

        alttext = bs.select('img')
        alttext = alttext[1].attrs
        alt = alttext['title']
        print(alt)

        text = bs.select('#middleContainer')
        textRe = re.compile(r'http.*\.png')
        aa = textRe.search(text[0].getText())
        imgform = 'png'
        if aa is None:
            textRe = re.compile(r'http.*\.jpg')
            aa = textRe.search(text[0].getText())
            imgform = 'jpg'


        initRe = re.compile(r'http://xk.*/')
        b = initRe.search(text[0].getText())

        bRe = re.compile(r'\d\d\d\d|\d\d\d|\d\d|\d')
        bb = bRe.search(b.group())

        count = int(bb.group())
        downImage(aa.group(),count,imgform,title,alt)


def downImage(a,count,imgform,title,alt):
    image = requests.get(a)
    image.raise_for_status()
    if imgform == 'png':
        filename = str(count)+'.png'
        ximage = open(filename,'wb')
    else:
        filename = str(count)+'.jpg'
        ximage = open(filename,'wb')
    for i in image.iter_content(100000):
        ximage.write(i)
    ximage.close()
    ximage = Image.open(filename)
    width, height = ximage.size
    xkcdFont = ImageFont.truetype('xkcd.otf',22)
    im = Image.new('RGBA', (width,70+height+160), 'black')
    im.paste(ximage, (0, 70))
    draw = ImageDraw.Draw(im)
    w,h = draw.textsize(title)
    draw.text(((width-w)/2-(w/2),35),title, fill='white', font=xkcdFont)
    cc = 20 
    widthh = 50
    if width<510:
        widthh = 40
    if width<410:
        widthh = 30
    for line in textwrap.wrap(alt, width=widthh):
        w,h = draw.textsize(line)
        draw.text(((width-w)/2-(w/2),70+height+cc),line, fill='white', font=xkcdFont)
        cc += 20
    im.save(filename)

xkcd(downlist)

