#!/usr/bin/env python
# -*- coding: utf-8 -*-
## Philipp Kats (c) June 2015

''' 
This script collects stats for specific wikipedia page
Using http://stats.grok.se/
'''

path = '/Users/casy/Dropbox/My_Projects/Karmatskiy_City/WikiGeoParser/data/result.csv'
rPath ='/Users/casy/Dropbox/My_Projects/Karmatskiy_City/WikiGeoParser/data/result_stats.csv'

import requests, lxml.html, csv
unique_keys = ('name', 'time')
errorLines = []

def getStats(lang, name, time):
    ''' gets stats for specific article'''
    baseLink = 'http://stats.grok.se/*/#/' # here 201506 can be replaced with any other month. * shall be replaced with the wiki language domain
    
    link = baseLink.replace('*', lang).replace('#', time) + name
    
    html = requests.get(link)
    if html.status_code != requests.codes.ok:
        print 'error with the link'
        errorLines.append(link)
        return None

    dom = lxml.html.fromstring(html.content)
    raw = dom.cssselect('p')[0].text_content().replace('\n', ' ').replace('\r', '').strip()
    print raw
    # seen
    s,e = raw.find('viewed')+7 , raw.find('times')-1
    seen = int(raw[s:e])
    # rank
    if 'ranked' in raw:
        s = raw.find('ranked')+7
        e = raw.find('in', s )-1
        # print s,e
        rank = int(raw[s:e])
    else:
        rank = None
    # print name, seen, rank
    # print name, 'ok'
    return {'link':link, 'lang':lang,'name':name, 'time':time, 'seen':seen, 'rank':rank}
    
# getStats('en','Luzhniki_Small_Sports_Arena', '201506')
rows = []
with open(path,'rb') as readFile:

    wD = csv.DictReader(readFile, fieldnames=None, restkey=None, restval=None, dialect='excel')
    
    for line in wD:
        line.update(getStats(line['feature'], line['name'], '201506')) 
        rows.append(line)

print 'parsed!'

headersList=rows[0].keys()

with open(rPath,'wb') as writeFile:
    wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
    wD.writeheader()

    for row in rows:
        wD.writerow(row)

print 'saved!'
for link in errorLines:
    print link