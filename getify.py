import urllib.request
import shutil
import os
import os.path
import zipfile
import time
import sys
import traceback
from subprocess import call
import base64
from bs4 import BeautifulSoup
import uuid
import html
import traceback

def find_between(file):
	f = open(file, "r", encoding = "utf8")
	soup = BeautifulSoup(f, 'html.parser')
	return soup.title

def download(link, file_name):
	"""Downloads web page from Wuxiaworld and saves it into the folder where the programm is located"""
	url = urllib.request.Request(
		link,
		data=None,
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
			}
		)
	with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)
	"""Extract Text from Wuxiaworld html file and saves it into a seperate xhtml file"""

def clean(file_name_in, file_name_out, start):
	suplementList = []
	has_spoiler = None
	raw = open(file_name_in, "r", encoding="utf8")
	soup = BeautifulSoup(raw, 'lxml')
	chapter_title = soup.find(class_="caption clearfix")
	chapter_title = chapter_title.find("h4")
	chapter_title = chapter_title.text
	# soups = soup.find_all(class_="fr-view")
	soups = soup.find(id="chapter-content")
	for block in soups:
		try:
			if block.name == 'script':
				block.extract()
				continue
			cpt = 1
			if block.name == 'img':
				tb = block['src'].split('?')[0].split('.')
				imgext = tb[len(tb) - 1]
				imgname = file_name_out + '_im{}'.format(cpt)+'.'+imgext
				tb = imgname.split('/')
				imgname2 = imgname.replace(tb[len(tb) - 1], 'images/'+tb[len(tb) - 1])
				print(block['src'])
				try:
					download(block['src'], imgname2)
					block['src'] = 'images/'+tb[len(tb) - 1]
					suplementList.append('images/'+tb[len(tb) - 1])
				except:
					traceback.print_exc()
				cpt += 1
		except Exception:
			""
			# block.extract() 
			
	soup = soups
	for a in soup.find_all("a"):
		a.decompose()
	raw.close()
	file = open(file_name_out + ".xhtml", "w", encoding="utf8")
	file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
	file.write("\n<head>")
	file.write('\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>')
	file.write("\n<title>" + chapter_title + "</title>")
	file.write("\n"+'<link href="common.css" rel="stylesheet" type="text/css"/>')
	file.write("\n</head>")
	file.write("\n<body>")
	file.write("\n<section>")
	file.write("\n<h1>" + chapter_title + "</h1>")
	file.write(str(soup).replace('<p></p>', '').replace('<p><br/></p>', '').replace('<hr>', ''))
	file.write("\n</section>")
	file.write("\n</body>")
	file.write("\n</html>")
	os.remove(file_name_in)
	return suplementList

def update_progress(progress):
	"""Displays and updates the download progress bar"""
	# This function is not used anymore but may be added later on.
	# Still fully functional though
	bar_length = 25  # Modify this to change the length of the progress bar
	status = ""
	if isinstance(progress, int):
		progress = float(progress)
	if not isinstance(progress, float):
		progress = 0
		status = "error: progress var must be float\r\n"
	if progress < 0:
		progress = 0
		status = "Halt...\r\n"
	if progress >= 1:
		progress = 1
		status = "Done...\r\n"
	block = int(round(bar_length*progress))
	text = "\rDownload Progress: [{0}] {1}% {2}".format( "#"*block + "-"*(bar_length-block), progress*100, status)
	sys.stdout.write(text)
	sys.stdout.flush()

def cover_generator(src, novel, book_name, author):
	""" This will download a cover, calculating the average complementary color
	and will wirte the chapter range on the upper half of the cover centered
	in the before mentioned color.
	Todo: Improve CCR to ignore bright parts of cover's that makes text sometimes hard to read.
	"""
	current_dir = os.path.dirname(os.path.realpath(__file__))
	storage_dir = current_dir
	if os.name == 'nt':
		storage_dir = os.path.expanduser("~") + os.sep + "wuxiaworld_export_ebook"
	if os.path.isdir(storage_dir + os.sep + "tmp") is False:
		os.mkdirs(storage_dir + os.sep + "tmp")
	print("Call URL :"+src);
	print("Store URL :"+storage_dir + os.sep + "tmp" + os.sep + "origin_cover");
	download(src, storage_dir + os.sep + "tmp" + os.sep + "origin_cover")
	
	file1 = open(storage_dir + os.sep + "tmp" + os.sep + "origin_cover", "rb")
	file2 = open(current_dir + os.sep + "ressources" + os.sep + "jacket.xhtml", "rb")
	file3 = open(storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml", "wb")
	cov = file1.read()
	jacket = file2.read()
	file2.close()
	covi = base64.b64encode(cov).decode('utf-8')
	ext = ""
	if covi.startswith('iVBOR') is True:
		ext = "data:image/png;base64,"
	elif covi.startswith('/9j/4AAQSkZJRgAB') is True:
		ext = "data:image/jpeg;base64,"
	jacket = jacket.decode('utf-8')
	jacket = jacket.replace('{novel}', novel)
	jacket = jacket.replace('{title}', book_name)
	jacket = jacket.replace('{author}', author)
	jacket = jacket.replace('{COVER}', ext+covi)
	file3.write(jacket.encode('utf-8')) 
	file3.close()
		
	try:
		call([
				sys.executable,
				current_dir + os.sep + "cover_generator" + os.sep + "exec.py",
				"-o",
				storage_dir + os.sep + "tmp" + os.sep + "cover.png",
				storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml"
			])
	except RuntimeError as e:
		traceback.print_exc()
		
	# os.remove(storage_dir + os.sep + "tmp" + os.sep + "origin_cover.jpg")
	# os.remove(storage_dir + os.sep + "tmp" + os.sep + "jacket.xhtml")

def generate_name(novelname, author, chaptername, book, chapter_s, chapter_e):
	file_name = ''
	if book is None:
		file_name = novelname + " - {}-{}".format(chapter_s, chapter_e)
	else:
		if chapter_s is None:
			file_name = novelname + " - {}".format(book)
		else:
			file_name = novelname + " - {} - {}-{}".format(book, chapter_s, chapter_e)
	return author + ' - ' + file_name

def generate(html_files, novelname, author, chaptername, book, chapter_s, chapter_e, suplementList, ebookFormat = 2):
	""" Saves downloaded xhtml files into the epub format while also
	generating the for the epub format nesessary container, table of contents,
	mimetype and content files
	ToDo: Generaliseing this part of the code and make it standalone accessible.
	SideNote: Will take a lot of time.
	"""
	current_dir = os.path.dirname(os.path.realpath(__file__))
	storage_dir = current_dir
	if os.name == 'nt':
		storage_dir = os.path.expanduser("~") + os.sep + "wuxiaworld_export_ebook"
	if os.path.isdir(storage_dir + os.sep + 'export') is False: os.mkdir(storage_dir + os.sep + 'export')
	file_name = ''
	if book is None: file_name = novelname + " - {}-{}".format(chapter_s, chapter_e)
	else:
		if chapter_s is None: file_name = novelname + " - {}".format(book)
		else: file_name = novelname + " - {} - {}-{}".format(book, chapter_s, chapter_e)
	
	file_name = file_name.replace(':', ',')
	epub = zipfile.ZipFile(storage_dir + os.sep + "export/" + author + ' - ' + file_name + ".epub", "w")
	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")
	"""
	The filenames of the HTML are listed in html_files
	We need an index file, that lists all other HTML files
	This index file itself is referenced in the META_INF/container.xml file
	"""
	opfFile = 'OEBPS/Content.opf'
	if ebookFormat >= 3: opfFile = 'metadata.opf'
	epub.writestr("META-INF/container.xml", '<container version="1.0" \
		xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\
		<rootfiles>\
			<rootfile full-path="'+ opfFile +'" media-type="application/oebps-package+xml"/>\
		</rootfiles>\
	</container>')
	# The index file is another XML file, living per convention
	# in OEBPS/Content.xml
	uniqueid = uuid.uuid1().hex
	file1 = open("./ressources/loading_fonts.txt", "r")
	font = file1.read()
	file1.close()
	fonsup = ''
	if ebookFormat >= 3: fonsup = 'font/'
	spinesup = ''
	if ebookFormat >= 3: spinesup = 'toc="ncx"'
	spinefirst = 'toc'
	if ebookFormat >= 3: spinefirst = 'start'
	index_tpl = '<?xml version=\'1.0\' encoding=\'utf-8\'?>\
	<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">\
			<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">\
				%(metadata)s\
			</metadata>\
			<manifest>\
				%(manifest)s\
				<item href="cover.png" id="cover" media-type="image/png" properties="cover-image"/>\
				<item href="common.css" id="commoncss" media-type="text/css"/>\
				<item href="'+fonsup +'Regular.ttf" id="font1" media-type="application/x-font-truetype"/>\
				<item href="'+fonsup +'Bold.ttf" id="font2" media-type="application/x-font-truetype"/>\
				<item href="'+fonsup +'Bold-Italic.ttf" id="font3" media-type="application/x-font-truetype"/>\
				<item href="'+fonsup +'Italic.ttf" id="font4" media-type="application/x-font-truetype"/>\
			</manifest>\
			<spine '+ spinesup +'>\
				<itemref idref="' + spinefirst + '"/>\
				%(spine)s\
			</spine>\
		</package>'
	manifest = ""
	toc_manifest = ""
	spine = ""
	navPoints = ""
	metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
		<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut"  ns0:file-as="%(author)s">%(author)s</dc:creator>
		<dc:language xmlns:dc="http://purl.org/dc/elements/1.1/">en</dc:language>
		<dc:identifier opf:scheme="uuid" id="uuid_id">%(uuid)s</dc:identifier>
		<dc:contributor opf:file-as="Wuxiaworld export Ebook" opf:role="bkp">Wuxiaworld export Ebook (2.x) [https://github.com/LordKBX/wuxiaworld_export_ebook]</dc:contributor>''' % { "novelname": file_name, "author": author, "uuid": uniqueid }
	if ebookFormat >= 3: 
		manifest += '<item href="start.xhtml" id="start" media-type="application/xhtml+xml"/>'
		toc_manifest += '<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>'
	else: 
		toc_manifest = '<item href="toc.xhtml" id="toc" properties="nav" media-type="application/xhtml+xml"/>'
	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
		basename = os.path.basename(html)
		manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (i+1, basename)
		spine += '<itemref idref="file_%s" />' % (i+1)
		navPoints += '<navPoint id="num_%(id)s" playOrder="%(id)s"> <navLabel><text>Chapter %(num)s</text></navLabel> <content src="%(file)s"/> </navPoint>' % { "id": i+2, "num": i+1, "file": basename  }
		if ebookFormat >= 3: epub.write(html, basename)
		else: epub.write(html, "OEBPS/"+basename)
	# Finally, write the index
	if ebookFormat >= 3: 
		epub.writestr("metadata.opf", index_tpl % { "metadata": metadata, "manifest": manifest + toc_manifest, "spine": spine })
		epub.writestr("start.xhtml", generate_toc(html_files, novelname))
		epub.write(storage_dir + os.sep + "tmp/cover.png", "cover.png")
		epub.writestr("toc.ncx", '''<?xml version='1.0' encoding='utf-8'?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1" xml:lang="fr">
  <head>
    <meta content="%(uuid)s" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="Wuxiaworld export Ebook (2.x) [https://github.com/LordKBX/wuxiaworld_export_ebook]" name="dtb:generator"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>Inconnu(e)</text>
  </docTitle>
  <navMap>
    <navPoint id="start" playOrder="1">
      <navLabel><text>Index</text></navLabel>
      <content src="start.xhtml"/>
    </navPoint>
	%(points)s
  </navMap>
</ncx>''' % { "uuid": uniqueid, "points":  navPoints })
	else: 
		epub.writestr("OEBPS/Content.opf", index_tpl % { "metadata": metadata, "manifest": manifest + toc_manifest, "spine": spine, })
		epub.writestr("OEBPS/toc.xhtml", generate_toc(html_files, novelname))
		epub.write(storage_dir + os.sep + "tmp/cover.png", "OEBPS/cover.png")
	
	try: os.remove(storage_dir + os.sep + "tmp/cover.png")
	except: {}
	
	file2 = open(storage_dir + os.sep + "ressources/common.css", "r")
	file3 = open(storage_dir + os.sep + "tmp/common.css", "w")
	ccss = file2.read()
	file2.close()
	ccss = ccss.replace('<FONT>', font)
	if ebookFormat >= 3:
		ccss = ccss.replace('Regular.ttf', 'font/Regular.ttf')
		ccss = ccss.replace('Bold-Italic.ttf', 'font/Bold-Italic.ttf')
		ccss = ccss.replace('Bold.ttf', 'font/Bold.ttf')
		ccss = ccss.replace('(Italic.ttf', '(font/Italic.ttf')
	file3.write(ccss) 
	file3.close()
	
	if ebookFormat >= 3:
		epub.write(storage_dir + os.sep + "tmp/common.css", "common.css")
		for img in suplementList:
			epub.write(storage_dir + os.sep + "tmp/"+img, img)
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Regular.ttf", "font/Regular.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Bold.ttf", "font/Bold.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Bold-Italic.ttf", "font/Bold-Italic.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Italic.ttf", "font/Italic.ttf")
	else:
		epub.write(storage_dir + os.sep + "tmp/common.css", "OEBPS/common.css")
		for img in suplementList:
			epub.write(storage_dir + os.sep + "tmp/"+img, "OEBPS/"+img)
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Regular.ttf", "OEBPS/Regular.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Bold.ttf", "OEBPS/Bold.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Bold-Italic.ttf", "OEBPS/Bold-Italic.ttf")
		epub.write(storage_dir + os.sep + "ressources/fonts/"+font+"/Italic.ttf", "OEBPS/Italic.ttf")
	
	try: os.remove(storage_dir + os.sep + "tmp/common.css")
	except: {}
	epub.close()
	# removes all the temporary files
	for x in html_files:
		try: os.remove(x)
		except: {}
	for img in suplementList:
		try: os.remove(storage_dir + os.sep + "tmp/"+img)
		except: {}
		
def unicodeToHTMLEntities(text):
    """Converts unicode to HTML entities.  For example '&' becomes '&amp;'."""
    text = html.escape(text, True).encode('ascii', 'xmlcharrefreplace').decode('ascii')
    return text

def generate_toc(html_files, novel):
	# Generates a Table of Contents + lost strings
	toc_start = '''<?xml version='1.0' encoding='utf-8'?>
		<!DOCTYPE html>
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
			<title>%(novelname)s</title>
			<link href="common.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
			<section class="frontmatter sectionCover">
				<img src="cover.png" alt="cover"/>
			</section>
			<section class="frontmatter TableOfContents">
				<header>
					<h1>Contents</h1>
				</header>
				<nav id="toc" role="doc-toc" epub:type="toc">
					<ol>
					%(toc_mid)s
			%(toc_end)s'''
	toc_mid = ""
	toc_end = '''</ol></nav></section></body></html>'''
	for i, y in enumerate(html_files):
		ident = 0
		chapter = find_between(html_files[i])
		chapter = unicodeToHTMLEntities( str(chapter).replace('title>', 'span>').replace('span>', '').replace('</', '').replace('<', '') )
		toc_mid += '''<li class="toc-Chapter-rw" id="num_%s">
			<a href="%s">%s</a>
			</li>''' % (i, os.path.basename(html_files[i]), chapter)
			
	return toc_start % {"novelname": unicodeToHTMLEntities(novel), "toc_mid": toc_mid, "toc_end": toc_end}
