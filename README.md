# XKCD-comic-downloader


A [XKCD](http://xkcd.xcom) comic downloader written in Python3.

+ It uses [Requests](http://docs.python-requests.org/en/master/) to download the pages and the comics.
+ It uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) to scrape the page for the alt-text and the title.
+ It automatically detects and downloads the comics that are not present in the current directory.
+ It uses [PILLOW](https://github.com/python-pillow/Pillow) to add the alt-text and title directly onto the image.
+ It uses the [XKCD typeface](http://log.danielignacio.me/xkcd-typeface) to make the addition look seamless.

Final Output:

![Sample](http://i.imgur.com/aawrPe5.png)
