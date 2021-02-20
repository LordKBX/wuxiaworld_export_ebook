import urllib.request
import shutil
import os
import os.path
import sys
import copy
from bs4 import BeautifulSoup
import html
		
def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = html.escape(text, True).encode('ascii', 'xmlcharrefreplace').decode('ascii')
    return text

def import_data(link: str, novel: str, limited: int):
	#link = 'https://www.wuxiaworld.com/novel/child-of-light'
	print(link)
	file_name = 'import.html'
	url = urllib.request.Request(
		link,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	f = open(file_name, "r", encoding="utf8")
	soup = BeautifulSoup(f, 'html.parser')
	with_volume = False
	books = {}
	alt_books = []
	tab = soup.find_all('ul')
	sttr = '{}'.format(tab)
	find1 = sttr.find('Chapter 1 ')
	exclude_list = ['Heavenly Jewel Change', 'God of Crime']
	if sttr.find('Chapter 1 ', find1+1) != -1 and novel not in exclude_list: with_volume = True
	else: books['Book 0'] = []
	
	firstLoop = True
	for block in tab:
		if limited == 1:
			if with_volume is False:
				if len(books['Book 0']) >= 45: break
			else:
				if firstLoop is False: break
				else: firstLoop = True
		tbl = '{}'.format(block)
		if tbl.find('list-chapters') != -1:
			tab2 = block.find_all('li')
			# print(tab2)
			last = '0'
			for li in tab2:
				if os.name == 'nt':
					print(unicodeToHTMLEntities(li.find('a').contents[0]));
				else:
					print(li.find('a').contents[0]);
				if with_volume is False:
					if limited == 1:
						if len(books['Book 0']) >= 45: break
					books['Book 0'].append({'name': li.find('a').contents[0].replace('\r', '').replace('\n', '').strip(), 'url': li.find('a').get('href')})
				else:
					span = li.find('a').contents[0]
					pos1 = span.find(',')
					pos2 = span.find(':')
					if pos1 == -1:
						if pos2 == -1: tb = [span]
						else: tb = span.split(':')
					elif pos2 == -1:
						if pos1 == -1: tb = [span]
						else: tb = span.split(',')
					else:
						if pos1 < pos2: tb = span.split(',')
						else: tb = span.split(':')
					if len(tb) < 2: 
						name = li.find('a').contents[0].replace('\r', '').replace('\n', '').strip()
						nbvol = last
					else:
						name = tb[1].strip()
						tb2 = tb[0].split(' ')
						nbvol = tb2[1]
						last = tb2[1]
					if int(float(nbvol)) < 10: nbvol = '0' + nbvol
					if 'Book '+nbvol not in books:
						books['Book '+nbvol] = []
					books['Book '+nbvol].append({'name': name, 'url': li.find('a').get('href')})
	#print(books)
	res = soup.find(id="accordion")
	tab = res.find_all('div')
	mb = {}
	for block in tab:
		tbl = '{}'.format(block)
		if tbl.find('panel panel-default') > -1:
			mb = {'title': block.find('a').contents[0].replace('\r', '').replace('\n', '').strip(), 'chapters': []}
			links = block.find_all('li')
			for li in links:
				tb2 = '{}'.format(li)
				if tb2.find('chapter-item') > -1:
					mb['chapters'].append({'name':li.find('a').contents[0].replace('\r', '').replace('\n', '').strip(), 'url':li.find('a').get('href')})
			alt_books.append(mb)
		if limited == 1: break
	#print(alt_books)
	soup.decompose()
	f.close()
	os.remove(file_name)
	return books, alt_books