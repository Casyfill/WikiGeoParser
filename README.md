Wikipedia Dump Geoparser
========================
####Philipp Kats, May 2015

## Describtion
This couple of scripts were written as part of [walkable streets](http://walkstreets.org/) project, lead by Andrew Karmatskiy.
First script parses wikipedia Json dump line by line with the use of **ijson** module, and return strings of data for only those who has geostatement within defined rectangluar. Then, second grabs stats for those pages from [stats.grok.se](http://stats.grok.se/).

##Dependencies
Scrip written in Python 2.7  with the use of [Ijson](https://pypi.python.org/pypi/ijson/)  for parsing big json files.

other modules used:
- requests
- lxtml.html
- csv

##How it works
1. First, download wikipedia dump as a json (i thing there is a way to read json from the archive directly)
2. Filter json with **streamJson.py**
3. Parse stats with **stats_parser.py**

For some reason, some of the articles were saved in dump several times. 

Also, please take in mind that streamJson works so stats are given for one page - russian if there is such, english if there is no russian but english exists, and any other (first in dict) if there is no englis neither russian page.

##Data source
- [Dump source](http://www.wikidata.org/wiki/Wikidata:Database_download)
- [more on data structure](http://www.mediawiki.org/wiki/Wikibase/DataModel/Primer#Ranks)
- [page views stats](http://stats.grok.se/)

* As you can notice, stats project allows to download raw stats data directly. However, I found myself stuck with this data encoding, so I find webscraping both easier and simpler.

