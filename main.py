# Multi-threaded python program to download xkcd comics, along with the heading and the alt-text.
__author__ = 'TheUbermanIsHere'


# The Program must check for all of the xkcd comics that have been downloaded uptill now.
# All the comics that are missing will be downloaded.
# The downloaded files must be saved as png's with their numbers as the filename.
# The comics title must be added to the top and the alt-text will be added to the bottom.

import re,os,requests,bs4

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
    dirlist.append(i)

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
print(text[0].getText())
textRe = re.compile('http://imgs.xkcd.com*')
aa = textRe.search(text[0].getText())
print(aa.group())

# Create a list of all the comics to be downloaded.


# Main-function that handles everything from downloading, to image processing, to saving the file.


# Get the Heading and the Alt-text.


# Image Processing


