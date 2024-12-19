#!/usr/bin/env python3
"""
Adapted from https://github.com/theubermanishere/xkcd-comic-downloader
by 'TheUbermanIsHere'

This script will take a comic number (or list of comic numbers) on the command-line 
and download the images for those comics.  It adds the alt-text and heading to the 
image.
"""
# Multi-threaded python program to download xkcd comics, along with the heading and the alt-text.
__author__ = ["TheUbermanIsHere", "jasoncausey"]

import re
import os
import requests
import bs4
import argparse
import unicodedata
from PIL import Image, ImageDraw, ImageFont
import textwrap


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to underscores. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "_", value).strip("-_")


def xkcd(a):
    for i in a:
        print("Currently downloading comic: " + str(i))
        page = requests.get("http://xkcd.com/" + str(i))
        page.raise_for_status()
        bs = bs4.BeautifulSoup(page.text, "lxml")
        title = bs.select("#ctitle")
        title = title[0].getText()
        print(title)

        alttext = bs.select("img")
        i = 1
        while "title" not in alttext[i].attrs:
            i += 1
        alttext = alttext[i].attrs

        alt = alttext["title"]
        print(alt)

        text = bs.select("#middleContainer")
        textRe = re.compile(r"http.*\.png")
        aa = textRe.search(text[0].getText())
        imgform = "png"
        if aa is None:
            textRe = re.compile(r"http.*\.jpg")
            aa = textRe.search(text[0].getText())
            imgform = "jpg"

        initRe = re.compile(r"https://xk.*/")
        b = initRe.search(text[0].getText())

        bRe = re.compile(r"\d\d\d\d|\d\d\d|\d\d|\d")
        bb = bRe.search(b.group())

        count = int(bb.group())
        downImage(aa.group(), count, imgform, title, alt)


def downImage(a, count, imgform, title, alt):
    image = requests.get(a)
    image.raise_for_status()
    file_base = slugify(title)
    if imgform == "png":
        filename = file_base + ".png"
        ximage = open(filename, "wb")
    else:
        filename = file_base + ".jpg"
        ximage = open(filename, "wb")
    for i in image.iter_content(100000):
        ximage.write(i)
    ximage.close()
    ximage = Image.open(filename)
    width, height = ximage.size
    font_size = 22
    xkcdFont = ImageFont.truetype("xkcd.otf", font_size)
    im = Image.new("RGBA", (width, 70 + height + 200), "black")
    im.paste(ximage, (0, 70))
    draw = ImageDraw.Draw(im)
    w = draw.textlength(title, font=xkcdFont)
    draw.text(((width - w) / 2, font_size + 10), title, fill="white", font=xkcdFont)
    widthh = 50
    if width < 551:
        widthh = 40
    if width < 461:
        widthh = 35
    if width < 410:
        widthh = 30
    if width < 360:
        widthh = 25
    if width < 310:
        widthh = 20
    for idx, line in enumerate(textwrap.wrap(alt, width=widthh)):
        line = line.strip()
        w = draw.textlength(line, font=xkcdFont)
        draw.text(
            ((width - w) / 2 , 70 + height + font_size * (idx+1)),
            line,
            fill="white",
            font=xkcdFont,
        )
    im.save(filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("comic_number", metavar="comic-number", type=str, nargs="+")
    args = parser.parse_args()
    comics = args.comic_number
    xkcd(comics)
