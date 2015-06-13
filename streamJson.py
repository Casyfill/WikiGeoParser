#!/usr/bin/env python
#-*- coding: utf-8 -*-

from ijson import items

path = '/Users/casy/Dropbox/My_Projects/Karmatskiy_City/WikiGeoParser/data/20150309.json'

def printLines(path, m=10):
	'''print first m lines from the big file'''
	count = 0
	with open(path) as infile:
	    for line in infile:
	    	if count>=m:
	    		break

	    	print line
	    	count+=1

def streamBigJson(path,m=50, geosquare=((-180,-180),(180,180)), writePath='result.csv'):
	'''stream big json from wikipedia dump json and save it to file.
	"m" param is the max items to proceed. If m=-1, limit is overrided'''
	import csv

	f = open(path,'r')
	objects = items(f, 'item')
	its = (o for o in objects if o['type'] == 'item')
	
	with open(writePath,'r') as rFile:
		alreadyWritten = max(len(list(rFile))-1,0)
	print 'already written: ', alreadyWritten

	headersList = ['id','name','link', 'lat','lon','precision', 'languages', 'lnum','feature', 'type']
	
	count = 0
	rCount = 0
	dfArray = []
	for i in its:

		for statement in i.get('claims',{}).values():
			for x in statement:
				if 'datatype' in x['mainsnak']:
					if x['mainsnak']['datatype']== 'globe-coordinate':

						lat, lon = (float(x['mainsnak']['datavalue']['value']['latitude']),float(x['mainsnak']['datavalue']['value']['longitude']))
						# check coordinate in square
						if inSquare( (lat,lon), geosquare, inside=False):
							break

						# skip already written ones
						rCount+=1
						if rCount <= alreadyWritten:
							break


						# parse id, link, coord, name
						# ID
						ID = i['id']
						# link
						# for link in i['sitelinks']: print link, i['sitelinks'][link]['title']
						link = '?'
						linkDict = {'ruwiki':'http://ru.wikipedia.org/wiki/','enwiki':'http://en.wikipedia.org/wiki/'}
						for t in linkDict:
							if t in i.get('sitelinks',{}): 	
								link = linkDict[t]  + i['sitelinks'][t]['title']
								# print link
								break
						if link == '?':
							if 'sitelinks' in i.keys():
								t = i['sitelinks'].keys()[0]
								link = t + '/' + i['sitelinks'][t]['title']
							else: 
								link = '?'
						

						
						# Languages
						languages = '|'.join([j for j in i['labels']]) # all languages
						lnum = len(i['labels']) #number of languages
						# print lnum, languages

						# coordTriad
						# lon, lat, precision
						coordPair = (lat,lon)
						cPrecision = x['mainsnak']['datavalue']['value']['precision']
						
						# name
						if 'ru' in i['labels']:
							feature = 'ru'
							name = i['labels']['ru']['value']
						elif 'en' in i['labels']:
							feature = 'en'
							name = i['labels']['en']['value']
						elif 'uk' in i['labels']:
							feature = 'en'
							name = i['labels']['uk']['value']
						else:
							feature = i['labels'].keys()[0]
							name = i['labels'][i['labels'].keys()[0]]['value']
						
						# print type(name)
						# print name
						# print type(name)==unicode 
						if type(name)!=unicode: name = unicode(name)
						# print type(name)==unicode
						T = defineType(name) 


						print count, rCount, name, T
						resRow = {'id':ID,
								  'name':name.encode('utf-8','ignore'),
								  'link':link.encode('utf-8','ignore'), 
								  'lat':coordPair[0],'lon':coordPair[1],
								  'precision':cPrecision, 
								  'languages':languages.encode('utf-8','ignore'), 
								  'lnum':lnum, 'feature':feature.encode('utf-8','ignore'), 
								  'type':T}
						
						with open(writePath,'a') as writeFile:
							wD = csv.DictWriter(writeFile, headersList,restval='', extrasaction='raise', dialect='excel')
							if alreadyWritten==0: 
								wD.writeheader()
								alreadyWritten=1

							wD.writerow(resRow)
						# for key in resRow: resRow[key]=unicode(resRow[key]).encode('utf-8','ignore')
						
						# save it
		# print count, rCount
		count+=1
		if m!=-1 and count>=m:
			break
	# return dfArray



def defineType(text):
	text = text.lower()

	ontology = {u'topo':[u'улица',u'мост',u'переулок',u'площадь',u'проезд',u'парк',u'сквер'],
				u'adm':[u'район',u'область',u'деревня',u'хутор',u'посёлок'],
				u'religion':[u'собор',u'церковь',u'часовня',u'монастырь',u'храм',u'синагога',u'мечеть'],
				u'event':[u'террористический',u'убийство',u'взрыв',u'обрушение',u'акция',u'митинг'],
				u'education':[u'университет',u'институт',u'школа',u'училище',u'академия'],
				u'transport':[u'аэропорт',u'вокзал']
				}

	for key in ontology.keys():
		for word in ontology[key]:
			if word in text: return key		

	return u'other'

		
	    
def inSquare(pair, geosquare=((-180,-180),(180,180)), inside=True ):
	'''returns if point in the geosquare'''
	if inside:
		return (geosquare[0][0]<=pair[0]<=geosquare[1][0] and geosquare[0][1]<=pair[1]<=geosquare[1][1])
	else:
		return not (geosquare[0][0]<=pair[0]<=geosquare[1][0] and geosquare[0][1]<=pair[1]<=geosquare[1][1])


Moscow = ((55.289547, 36.635486),(56.239792, 38.882190))
test = ((45.567273, 21.430408),(59.433441, 46.215564))
print 'started!'

writeFile = '/Users/casy/Dropbox/My_Projects/Karmatskiy_City/WikiGeoParser/data/result.csv'

# print defineType('террористический лалала'.decode('utf-8','ignore'))
streamBigJson(path, m=-1, geosquare=Moscow, writePath=writeFile)
# print inSquare((190,0), ((-180,-180),(180,180)))

# SAVING



print 'done here!'