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
import PIL

# Create a list of all the files that are present in the current directory.

pngReg = re.compile(r'[a-zA-Z0-9]*.png')
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

downlist = list(i for i in range(131,counter))
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
        print(title[0].getText())

        alttext = bs.select('img')
        alttext = alttext[1].attrs
        print(alttext['title'])

        text = bs.select('#middleContainer')
        textRe = re.compile(r'http.*\.(png|jpg)')
        aa = textRe.search(text[0].getText())

        initRe = re.compile(r'http://xk.*/')
        b = initRe.search(text[0].getText())
        print(b.group())

        bRe = re.compile(r'\d\d\d\d|\d\d\d|\d\d|\d')
        bb = bRe.search(b.group())
        print(bb.group())

        count = int(bb.group())
        downImage(aa.group(), count)





# Main-function that handles everything from downloading, to image processing, to saving the file.
def downImage(a, count):
    image = requests.get(a)
    image.raise_for_status()
    ximage = open(str(count)+'.png','wb')
    for i in image.iter_content(100000):
        ximage.write(i)
    ximage.close()

xkcd(downlist)

# Get the Heading and the Alt-text.


# Image Processing


