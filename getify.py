import urllib.request
import shutil
import os
import os.path
import zipfile
import time
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from bs4 import BeautifulSoup
import uuid

def find_between(file):
	f = open(file, "r", encoding = "utf8")
	soup = BeautifulSoup(f, 'html.parser')
	return soup.title


"""Downloads web page from Wuxiaworld and saves it into the folder where the programm is located"""
def download(link, file_name):
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
	has_spoiler = None
	raw = open(file_name_in, "r", encoding = "utf8")
	soup = BeautifulSoup(raw, 'lxml')
	chapter_title = soup.find(class_="caption clearfix")
	chapter_title = chapter_title.find("h4")
	chapter_title = chapter_title.text
	soup = soup.find(class_="fr-view")
	for a in soup.find_all("a"):
		a.decompose()
	raw.close()
	file = open(file_name_out + ".xhtml", "w", encoding = "utf8")
	file.write('<html xmlns="http://www.w3.org/1999/xhtml">')
	file.write("\n<head>")
	file.write("\n<title>" + chapter_title + "</title>")
	file.write("\n"+'<link href="common.css" rel="stylesheet" type="text/css"/>')
	file.write("\n</head>")
	file.write("\n<body>")
	file.write("\n<h1>" + chapter_title + "</h1>")
	file.write(str(soup).replace('<p></p>', '').replace('<p><br></p>', '').replace('<hr>', ''))
	file.write("\n</body>")
	file.write("\n</html>")
	os.remove(file_name_in)


"""Displays and updates the download progress bar"""
# This function is not used anymore but may be added later on.
# Still fully functional though
def update_progress(progress):
	barLength = 25 # Modify this to change the length of the progress bar
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
	block = int(round(barLength*progress))
	text = "\rDownload Progress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
	sys.stdout.write(text)
	sys.stdout.flush()


""" This will download a cover, calculating the average complementary color
	and will wirte the chapter range on the upper half of the cover centered
	in the before mentioned color.
	Todo: Improve CCR to ignore bright parts of cover's that makes text sometimes
	hard to read."""


def cover_generator(src, msg1, msg2, msg3, msg4):
	if os.path.isdir('./tmp') is False:
		os.mkdir('./tmp')
	urllib.request.urlretrieve(src, "./tmp/cover.jpg")
	img = Image.open("./tmp/cover.jpg")
	draw = ImageDraw.Draw(img)
	thefont = ImageFont.truetype("arial.ttf", 28)
	thefont2 = ImageFont.truetype("arial.ttf", 50)
	#Get's the average complementary color of the picutre
	W, H = (400, 600)
	img2 = img.resize((1, 1))
	redc = 255 - img2.getpixel((0, 0))[0]
	greebc = 255 - img2.getpixel((0, 0))[1]
	bluec = 255 - img2.getpixel((0, 0))[2]
	complementary = (redc, greebc, bluec)
	w, h = draw.textsize(msg1, font=thefont)
	draw.text(((W - w) / 2, 432), msg1, complementary, font = thefont)
	w, h = draw.textsize(msg2, font=thefont)
	draw.text(((W - w) / 2, 465), msg2, complementary, font = thefont)
	w, h = draw.textsize(msg3, font=thefont2)
	draw.text(((W - w) / 2, 500), msg3, complementary, font = thefont2)
	w, h = draw.textsize(msg4, font=thefont)
	draw.text(((W - w) / 2, 550), msg4, complementary, font = thefont)
	img.save("./tmp/cover.jpg")


""" Saves downloaded xhtml files into the epub format while also
	generating the for the epub format nesessary container, table of contents,
	mimetype and content files
	ToDo: Generaliseing this part of the code and make it standalone accessible.
	Sidenote: Will take a lot of time."""


def generate(html_files, novelname, author, chaptername, book, chapter_s, chapter_e):
	if os.path.isdir('./export') is False:
		os.mkdir('./export')
	fileName = ''
	if book is None:
		fileName = author + ' - ' + novelname + " - {}-{}".format(chapter_s, chapter_e)
	else:
		if chapter_s is None:
			fileName = author + ' - ' + novelname + " - {}".format(book)
		else:
			fileName = author + ' - ' + novelname + " - {} - {}-{}".format(book, chapter_s, chapter_e)
	fileName = fileName.replace(':',',')
	epub = zipfile.ZipFile("./export/" + fileName + ".epub", "w")
	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")

	 # The filenames of the HTML are listed in html_files
	# We need an index file, that lists all other HTML files
	# This index file itself is referenced in the META_INF/container.xml
	# file
	epub.writestr("META-INF/container.xml", '''<container version="1.0"
				  xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
		  <rootfiles>
			<rootfile full-path="OEBPS/Content.opf" media-type="application/oebps-package+xml"/>
		  </rootfiles>
		</container>''')

	# The index file is another XML file, living per convention
	# in OEBPS/Content.xml
	uniqueid = uuid.uuid1().hex
	index_tpl = '''<package version="3.1"
	xmlns="http://www.idpf.org/2007/opf" unique-identifier="''' + uniqueid + '''">
			<metadata>
				%(metadata)s
			</metadata>
			<manifest>
				%(manifest)s
				<item href="cover.jpg" id="cover" media-type="image/jpeg" properties="cover-image"/>
				<item href="common.css" id="commoncss" media-type="text/css"/>
				<item href="Century-Gothic.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Century-Gothic-Bold.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Century-Gothic-Bold-Italic.ttf" id="id1" media-type="application/font-sfnt"/>
				<item href="Century-Gothic-Italic.ttf" id="id1" media-type="application/font-sfnt"/>
			</manifest>
			<spine>
				<itemref idref="toc"/>
				%(spine)s
			</spine>
		</package>'''

	manifest = ""
	spine = ""
	metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
		<dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut" ns0:file-as="Unbekannt">%(author)s</dc:creator>
		<dc:language xmlns:dc="http://purl.org/dc/elements/1.1/">en</dc:language>
		<dc:identifier xmlns:dc="http://purl.org/dc/elements/1.1/">%(uuid)s"</dc:identifier>''' % {
		"novelname": fileName, "author": author, "uuid": uniqueid}
	toc_manifest = '<item href="toc.xhtml" id="toc" properties="nav" media-type="application/xhtml+xml"/>'

	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
		basename = os.path.basename(html)
		manifest += '<item id="file_%s" href="%s" media-type="application/xhtml+xml"/>' % (
					  i+1, basename)
		spine += '<itemref idref="file_%s" />' % (i+1)
		epub.write(html, "OEBPS/"+basename)

	# Finally, write the index
	epub.writestr("OEBPS/Content.opf", index_tpl % {
		"metadata": metadata,
		"manifest": manifest + toc_manifest,
		"spine": spine,
		})

 #Generates a Table of Contents + lost strings
	toc_start = '''<?xml version='1.0' encoding='utf-8'?>
		<!DOCTYPE html>
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
		<head>
			<title>%(novelname)s</title>
			<link href="common.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
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
		chapter = str(chapter).replace('title>', 'span>')
		toc_mid += '''<li class="toc-Chapter-rw" id="num_%s">
			<a href="%s">%s</a>
			</li>''' % (i, html_files[i], chapter)

	epub.writestr("OEBPS/toc.xhtml", toc_start % {"novelname": novelname, "toc_mid": toc_mid, "toc_end": toc_end})
	
	epub.write("./tmp/cover.jpg", "OEBPS/cover.jpg")
	os.remove("./tmp/cover.jpg")
	
	epub.write("./ressources/common.css", "OEBPS/common.css")
	epub.write("./ressources/Century-Gothic.ttf", "OEBPS/Century-Gothic.ttf")
	epub.write("./ressources/Century-Gothic-Bold.ttf", "OEBPS/Century-Gothic-Bold.ttf")
	epub.write("./ressources/Century-Gothic-Bold-Italic.ttf", "OEBPS/Century-Gothic-Bold-Italic.ttf")
	epub.write("./ressources/Century-Gothic-Italic.ttf", "OEBPS/Century-Gothic-Italic.ttf")
	
	epub.close()

	#removes all the temporary files
	for x in html_files:
		os.remove(x)
