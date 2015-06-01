#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ijson import items

path = '/Users/casy/Dropbox/My_Projects/Karmatskiy_City/wiki/20150309.json'

def printLines(path, m=10):
	'''print first m lines from the big file'''
	count = 0
	with open(path) as infile:
	    for line in infile:
	    	if count>=m:
	    		break

	    	print line
	    	count+=1

def streamBigJson(path,m=50, geosquare=((-180,-180),(180,180))):
	'''stream big json from wikipedia dump json'''
	f = open(path,'r')
	objects = items(f, 'item')
	print 'done getting objects'
	its = (o for o in objects if o['type'] == 'item')
	# its = objects
	print 'done getting its'
	count = 0

	for i in its:
		for statement in i['claims'].values():
			for x in statement:
				if 'datatype' in x['mainsnak']:
					if x['mainsnak']['datatype']== 'globe-coordinate':

						lat, lon = (float(x['mainsnak']['datavalue']['value']['latitude']),float(x['mainsnak']['datavalue']['value']['longitude']))
						# check coordinate in square
						if inSquare( (lat,lon), geosquare, inside=False):
							break

						# parse id, link, coord, name
						# ID
						ID = i['id']
						# link
						# for link in i['sitelinks']: print link, i['sitelinks'][link]['title']
						for t in ['ruwiki','enwiki','enwikiquote']:
							if t in i['sitelinks']: 	
								link = t + '/' + i['sitelinks'][t]['title']
								# print link
								break
						

						
						# Languages
						languages = '|'.join([j for j in i['labels']]) # all languages
						lnum = len(i['labels']) #number of languages
						# print lnum, languages

						# coordTriad
						# lon, lat, precision
						coordPair = (lat,lon)
						# print type(x['mainsnak']['datavalue']['value']['latitude'])
						cPrecision = x['mainsnak']['datavalue']['value']['precision']
						# name
						if 'ru' in i['labels']:
							name = i['labels']['ru']['value']
						elif 'en' in i['labels']:
							name = i['labels']['en']['value']
						else:
							name = 'unknown'
						
						print name, link, coordPair, cPrecision
						# save it
				
		count+=1
		if count>=m:
			break
	    
def inSquare(pair, geosquare=((-180,-180),(180,180)), inside=True ):
	'''returns if point in the geosquare'''
	if inside:
		return (geosquare[0][0]<=pair[0]<=geosquare[1][0] and geosquare[0][1]<=pair[1]<=geosquare[1][1])
	else:
		return not (geosquare[0][0]<=pair[0]<=geosquare[1][0] and geosquare[0][1]<=pair[1]<=geosquare[1][1])


Moscow = ((55.289547, 36.635486),(56.239792, 38.882190))
test = ((45.567273, 21.430408),(59.433441, 46.215564))
print 'started!'
# printLines(path)
streamBigJson(path, m=1000, geosquare=Moscow)
# print inSquare((190,0), ((-180,-180),(180,180)))
print 'done here!'