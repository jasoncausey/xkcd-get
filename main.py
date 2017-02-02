# Multi-threaded python program to download xkcd comics, along with the heading and the alt-text.
__author__ = 'TheUbermanIsHere'

# The Program must check for all of the xkcd comics that have been downloaded uptill now.
# All the comics that are missing will be downloaded.
# The downloaded files must be saved as png's with their numbers as the filename.
# The comics title must be added to the top and the alt-text will be added to the bottom.

import re
import os
import requests
import bs4
from PIL import Image,ImageDraw,ImageFont
import textwrap

# Create a list of all the files that are present in the current directory.

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

# Go to the homepage and check the number of the latest comic, and initialize a counter with the number.

home = requests.get('http://xkcd.com')
home.raise_for_status()
bs = bs4.BeautifulSoup(home.text,"lxml")
title = bs.select('#ctitle')
print(title[0].getText())

alttext = bs.select('img')
alttext = alttext[1].attrs
print(alttext['title'])

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

# The Download list has been initialized.
# Function that download the comics from the given list.

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
        print(b.group())

        bRe = re.compile(r'\d\d\d\d|\d\d\d|\d\d|\d')
        bb = bRe.search(b.group())
        print(bb.group())

        count = int(bb.group())
        downImage(aa.group(),count,imgform,title,alt)


# Main-function that handles everything from downloading, to image processing, to saving the file.
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
    arvo = ImageFont.truetype('xkcd.otf',22)
    im = Image.new('RGBA', (width,70+height+160), 'black')
    im.paste(ximage, (0, 70))
    draw = ImageDraw.Draw(im)
    w,h = draw.textsize(title)
    draw.text(((width-w)/2-(w/2),35),title, fill='white', font=arvo)
    cc = 20 
    widthh = 50
    if width<510:
        widthh = 40
    if width<410:
        widthh = 30
    for line in textwrap.wrap(alt, width=widthh):
        w,h = draw.textsize(line)
        draw.text(((width-w)/2-(w/2),70+height+cc),line, fill='white', font=arvo)
        cc += 20
    im.save(filename)

xkcd(downlist)

# To-do:
# 1. Get the size of the image.
# 2. Figure out the size of the text that must be pasted
# 3. Open a new image, and paste the downloaded image on top of that
# 4. Put the heading and the alt-text in place.
# 5. Save the Image as a png file.

