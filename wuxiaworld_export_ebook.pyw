import os
import os.path
import sys
import sqlite3 as sql
import traceback
from urllib.error import HTTPError, URLError
import time
import subprocess
from PyQt4 import QtCore, QtGui
import ctypes

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + os.sep + 'interfaces')
import interface
import infoBox
import novel_data
import database_updator
import getify

conn = None
cursor = None

novel = ''
data_novel = {}
app = None
app_icon =None
window = None
dialog = None
generating = False
styleUpdateGrey = "background-color:#CCCCCC;color:#000000;"
styleUpdateGreen = 'background-color:#55AA00;color: #ffffff;'
threadpool = None
outdatedScript = False

class WorkerSignals(QtCore.QObject):
	'''
	Defines the signals available from a running worker thread.

	Supported signals are:

	finished
		No data

	error
		`tuple` (exctype, value, traceback.format_exc() )

	result
		`object` data returned from processing, anything

	progress
		`int` indicating % progress

	'''
	finished = QtCore.pyqtSignal()
	error = QtCore.pyqtSignal(tuple)
	result = QtCore.pyqtSignal(object)
	progress = QtCore.pyqtSignal(list)

class Worker(QtCore.QRunnable):
	'''
	Worker thread

	Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

	:param callback: The function callback to run on this worker thread. Supplied args and 
					 kwargs will be passed through to the runner.
	:type callback: function
	:param args: Arguments to pass to the callback function
	:param kwargs: Keywords to pass to the callback function

	'''

	def __init__(self, fn, *args, **kwargs):
		super(Worker, self).__init__()

		# Store constructor arguments (re-used for processing)
		self.fn = fn
		self.args = args
		self.kwargs = kwargs
		self.signals = WorkerSignals()

		# Add the callback to our kwargs
		self.kwargs['progress_callback'] = self.signals.progress

	@QtCore.pyqtSlot()
	def run(self):
		'''
		Initialise the runner function with passed args, kwargs.
		'''

		# Retrieve args/kwargs here; and fire processing using them
		try:
			result = self.fn(*self.args, **self.kwargs)
		except:
			traceback.print_exc()
			exctype, value = sys.exc_info()[:2]
			self.signals.error.emit((exctype, value, traceback.format_exc()))
		else:
			self.signals.result.emit(result)  # Return the result of the processing
		finally:
			self.signals.finished.emit() 
	
def worker_progress(status):
	updateStatus(status[0])
	try: print(status[0])
	except: {}
	try: dialog.statusProgressBar.setProperty("value", status[1])
	except: {}

def worker_print_output(s):
	print(s)

def exitWindow():
	global generating, window
	window.close()
	
def updateStatus(message:str, green=False):
	global dialog, styleUpdateGrey, styleUpdateGreen
	try:
		if green is True: dialog.statusLabel.setStyleSheet(interface._fromUtf8(styleUpdateGreen))
		else: dialog.statusLabel.setStyleSheet(interface._fromUtf8(styleUpdateGrey))
		dialog.statusLabel.setText(message)
	except:{}
	
def infoDialog(title, message, modal=True):
	global app_icon
	#if modal is True:
	dialog = infoBox.Ui_Dialog()
	window = QtGui.QDialog()
	dialog.setupUi(window)
	window.setWindowTitle(title)
	window.setWindowIcon(app_icon)
	window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
	dialog.label_2.setText(message)
	dialog.pushButton.clicked.connect(window.close)
	window.exec_()

def check_script_version():
	global outdatedScript
	outdatedScript = False
	print('> Check script update')
	worker = Worker(check_script_version_mid) # Any other args, kwargs are passed to the run function
	worker.signals.finished.connect(check_script_version_end)
	worker.signals.progress.connect(worker_progress)
	threadpool.start(worker)


def check_script_version_mid(progress_callback):
	global outdatedScript
	file_version_online = './check_version.txt'
	try:
		getify.download('https://raw.githubusercontent.com/LordKBX/wuxiaworld_export_ebook/master/version.txt', file_version_online)
	except HTTPError as e:
		# Return code error (e.g. 404, 501, ...)
		print('URL: {}, HTTPError: {} - {}'.format(bulk_list[x]['url'], e.code, e.reason))
	except URLError as e:
		# Not an HTTP-specific error (e.g. connection refused)
		print('URL: {}, URLError: {}'.format(bulk_list[x]['url'], e.reason))
	else:
		file1  = open("./version.txt", "r")
		file2  = open(file_version_online, "r")
		version_locale = file1.read()
		version_online = file2.read()
		file1.close()
		file2.close()
		if version_locale not in version_online:
			outdatedScript = True

def check_script_version_end():
	global outdatedScript
	if outdatedScript is True:
		infoDialog('Update', '<html><head/><body><p>A new version of the script is online</p><p><a href="https://github.com/LordKBX/wuxiaworld_export_ebook"><span style=" text-decoration: underline; color:#0000ff;">https://github.com/LordKBX/wuxiaworld_export_ebook</span></a></p></body></html>')
	else: print('< Script up to date')

def check_database():
	global generating
	if time.time() - float(os.path.getmtime("novels.db")) >= 43200.0: #test 43200 = 12h
		generating = True
		worker = Worker(check_database_mid) # Any other args, kwargs are passed to the run function
		worker.signals.finished.connect(check_database_end)
		worker.signals.progress.connect(worker_progress)
		threadpool.start(worker)
		infoDialog('Info', 'Start database update', False)
	else: check_database_final()
		
def check_database_mid(progress_callback):
	print('> Updating Novel Database')
	database_updator.parent = progress_callback
	database_updator.start()

def check_database_end():
	os.utime("novels.db")
	status = "Database Update, Task finished at {}".format(time.asctime())
	updateStatus(status, True)
	print(status)
	dialog.statusProgressBar.setProperty("value", 100)
	check_database_final()

def check_database_final():
	global conn, cursor, generating
	generating = False
	conn = sql.connect("novels.db")
	cursor = conn.cursor()
	cursor.execute("SELECT NovelName FROM 'Information' ORDER BY NovelName ASC")
	db = cursor.fetchall()
	namelist = ['']
	for i in db:
		namelist.append(i[0])
		namelist.sort()
	dialog.novelSelector.clear()
	dialog.novelSelector.addItems(namelist)

def changeFont():
	global dialog
	curFont = dialog.fontSelector.currentText()
	try:
		if curFont not in QtGui.QFontDatabase().families():
			font_db = QtGui.QFontDatabase()
			font_db.addApplicationFont('./ressources/fonts/'+curFont+'/Regular.ttf')
			font_db.addApplicationFont('./ressources/fonts/'+curFont+'/Italic.ttf')
			font_db.addApplicationFont('./ressources/fonts/'+curFont+'/Bold.ttf')
			font_db.addApplicationFont('./ressources/fonts/'+curFont+'/Bold-Italic.ttf')
			
		font1 = QtGui.QFont(curFont,pointSize=10)
		font2 = QtGui.QFont(curFont,pointSize=10, italic=True)
		font3 = QtGui.QFont(curFont,pointSize=10)
		font3.setBold(True)
		font3.setWeight(75)
		font4 = QtGui.QFont(curFont,pointSize=10, italic=True)
		font4.setBold(True)
		font4.setWeight(75)
		
		dialog.fontLabelPreview_1.setFont(font1)
		dialog.fontLabelPreview_2.setFont(font2)
		dialog.fontLabelPreview_3.setFont(font3)
		dialog.fontLabelPreview_4.setFont(font4)
		file1  = open("./ressources/loading_fonts.txt", "w")
		file1.write(curFont) 
		file1.close()
	except: 
		traceback.print_exc()

def lockInterface(full=False):
	global dialog
	if full is True:
		dialog.novelSelector.setEnabled(False)
	dialog.modeSlider.setEnabled(False)
	dialog.totalExportSlider.setEnabled(False)
	dialog.bookSelector.setEnabled(False)
	dialog.startingChapterSelector.setEnabled(False)
	dialog.endingChapterSelector.setEnabled(False)
	dialog.fontSelector.setEnabled(False)
	
def unlockInterface():
	global dialog
	dialog.novelSelector.setEnabled(True)
	dialog.modeSlider.setEnabled(True)
	dialog.totalExportSlider.setEnabled(True)
	dialog.fontSelector.setEnabled(True)

def changeNovel():
	global novel, cursor, data_novel
	novel = dialog.novelSelector.currentText()
	if novel != "":
		lockInterface()
		cursor.execute("SELECT link,autor,cover,limited FROM 'Information' WHERE NovelName LIKE ?", (novel,))
		db = cursor.fetchall()
		data_novel={}
		for i in db:
			data_novel['link'] = i[0]
			data_novel['autor'] = i[1]
			data_novel['cover'] = i[2]
			data_novel['limited'] = i[3]
			break
		if data_novel['limited'] == 1:
			infoDialog('Information', "You have select a WuxiaWorld original novel.\nBecause they sell ebooks of their originals novel(on Amazon), you would be limited to the first 45 chapters in classic mode or the first book in alternate mode")
			#QtGui.QMessageBox.question(None, 'Information', "You have select a WuxiaWorld original novel.\n" +
			#"Because they sell ebooks of their originals novel(on Amazon), you would be limited to the first 45 chapters in classic mode or the first book in alternate mode", QtGui.QMessageBox.Ok)
		
		QtCore.QTimer.singleShot(200, changeNovelPart2)
		
def changeNovelPart2():
	global novel, data_novel
	data_novel['books'], data_novel['alt_books'] = novel_data.import_data(data_novel['link'], novel, data_novel['limited'])
	unlockInterface()
	export_mode_change()
	updateStatus( "Data for novel '{}' loaded at {}".format( novel, time.asctime() ) )
	
def export_mode_change():
	global dialog, novel, cursor, data_novel
	export_mode = dialog.modeSlider.value()
	export_full = dialog.totalExportSlider.value()
	if 'books' not in data_novel: return
	if export_full == 0:
		if export_mode == 0:
			dialog.bookSelector.clear()
			dialog.bookSelector.addItems(sorted(data_novel['books']))
			if 'Book 01' in data_novel['books']: dialog.bookSelector.setEnabled(True)
			else: dialog.bookSelector.setEnabled(False)
			try:dialog.bookSelector.setCurrentIndex(0)
			except:{}
			book_change()
		else:
			books_list = []
			for block in data_novel['alt_books']:
				books_list.append(block['title'])
			dialog.bookSelector.clear()
			dialog.bookSelector.addItems(books_list)
			dialog.bookSelector.setEnabled(True)
			try:dialog.bookSelector.setCurrentIndex(0)
			except:{}
			book_change()
	else:
		dialog.bookSelector.clear()
		dialog.bookSelector.addItems([])
		dialog.bookSelector.setEnabled(False)
		dialog.startingChapterSelector.clear()
		dialog.startingChapterSelector.addItems([])
		dialog.startingChapterSelector.setEnabled(False)
		dialog.endingChapterSelector.clear()
		dialog.endingChapterSelector.addItems([])
		dialog.endingChapterSelector.setEnabled(False)
		
def book_change():
	global dialog, novel, cursor, data_novel
	export_mode = dialog.modeSlider.value()
	book = dialog.bookSelector.currentText()
	chapters = []
	if export_mode == 0:
		if book in data_novel['books']:
			for bl in data_novel['books'][book]:
				chapters.append(bl['name'])
	else:
		for block in data_novel['alt_books']:
			if block['title'] == book:
				for bl in block['chapters']:
					chapters.append(bl['name'])
	
	dialog.startingChapterSelector.clear()
	dialog.startingChapterSelector.addItems(chapters)
	dialog.startingChapterSelector.setEnabled(True)
	dialog.startingChapterSelector.setCurrentIndex(0)
	dialog.endingChapterSelector.clear()
	dialog.endingChapterSelector.addItems(chapters)
	dialog.endingChapterSelector.setEnabled(True)
	dialog.endingChapterSelector.setCurrentIndex(len(chapters) - 1)

def preview():
	global dialog, app, novel, cursor, data_novel, generating
	if generating is True: return
	if novel == '':
		infoDialog('Information', "Function availlable only if a novel was selected")
		return
	app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
	book = dialog.bookSelector.currentText()
	
	getify.cover_generator(data_novel['cover'], novel, book, data_novel['autor'])
		
	file2  = open("./ressources/common.css", "r")
	css = file2.read()
	file2.close()
	file3  = open("./tmp/common.css", "w")
	file3.write(css.replace('<FONT>', dialog.fontSelector.currentText()))
	file3.close()
	
	link = ''
	
	link = data_novel['books'][book][0]['url']
	ti = link.split('/')
	filename = "./tmp/"+ti[len(ti) - 1] + ".xhtml"
	filenameOut = "./tmp/"+'ch-{}'.format(1)
	
	try:
		getify.download('https://www.wuxiaworld.com' + link, filename)
	except HTTPError as e:
		# Return code error (e.g. 404, 501, ...)
		print('URL: {}, HTTPError: {} - {}'.format(bulk_list[x]['url'], e.code, e.reason))
	except URLError as e:
		# Not an HTTP-specific error (e.g. connection refused)
		print('URL: {}, URLError: {}'.format(bulk_list[x]['url'], e.reason))
	else:
		getify.clean(filename, filenameOut, novel)
		filenameOut += ".xhtml"
		text_toc = getify.generate_toc([filenameOut,filenameOut,filenameOut,filenameOut,filenameOut,filenameOut,filenameOut,filenameOut], novel)
		file3  = open("./tmp/toc.xhtml", "w")
		file3.write(text_toc)
		file3.close()
		command1 = subprocess.Popen([sys.executable, "./css_editor/launch.py"])
	app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
	
def generate():
	global dialog, novel, data_novel, generating, threadpool
	if generating is True: return
	if novel == '': return
	lockInterface(True)
	app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
	status = "Start ebook generation at {}".format( novel, time.asctime() )
	updateStatus(status)
	print(status)
	generating = True
	
	worker = Worker(generate_mid) # Any other args, kwargs are passed to the run function
	worker.signals.result.connect(worker_print_output)
	worker.signals.finished.connect(generate_end)
	worker.signals.progress.connect(worker_progress)

	# Execute
	threadpool.start(worker)
	
def generate_mid(progress_callback):
	global dialog, novel, data_novel
	export_mode = dialog.modeSlider.value()
	export_full = dialog.totalExportSlider.value()
	book = dialog.bookSelector.currentText()
	chapter_start = dialog.startingChapterSelector.currentText()
	chapter_end = dialog.endingChapterSelector.currentText()
	
	#title = novel
	#data_novel['books'], data_novel['alt_books']
	msg1 = ''
	msg2 = ''
	msg3 = ''
	bulk_list = []
	file_list = []
	if export_full == 0:
		if export_mode == 0:
			if book == '':
				book = 'Book 0'
			if book != 'Book 0':
				msg1 = book
			good = False
			for bok in data_novel['books'][book]:
				if good is True or bok['name'] == chapter_start:
					good = True
					bulk_list.append(bok)
					if bok['name'] == chapter_end: good = False
		else:#Mode Alternatif
			msg1 = book
			for block in data_novel['alt_books']:
				good = False
				if block['title'] == book:
					for bl in block['chapters']:
						if good is True or bl['name'] == chapter_start:
							good = True
							bulk_list.append(bl)
							if bl['name'] == chapter_end: good = False
				
		bookName = chapter_start + "<br/>=><br/>" + chapter_end
		
		cover = data_novel['cover']
		if cover[0] == '/':
			cover = 'https://cdn.wuxiaworld.com' + cover
		
		progress_callback.emit(['generating cover ...', 10])
		getify.cover_generator(data_novel['cover'], novel, bookName, data_novel['autor'])
		
		step = (100 - 22) / len(bulk_list)
		pos = 10
		
		for x in range(len(bulk_list)):
			pos += step
			progress_callback.emit(['Downloading {}'.format(bulk_list[x]['name']), pos])
			ti = bulk_list[x]['url'].split('/')
			filename = "./tmp/"+ti[len(ti) - 1] + ".xhtml"
			filenameOut = "./tmp/"+'ch-{}'.format(x+1)
			try:
				getify.download('https://www.wuxiaworld.com' + bulk_list[x]['url'], filename)
			except HTTPError as e:
				# Return code error (e.g. 404, 501, ...)
				print('URL: {}, HTTPError: {} - {}'.format(bulk_list[x]['url'], e.code, e.reason))
			except URLError as e:
				# Not an HTTP-specific error (e.g. connection refused)
				print('URL: {}, URLError: {}'.format(bulk_list[x]['url'], e.reason))
			else:
				getify.clean(filename, filenameOut, novel)
				file_list.append(filenameOut + ".xhtml")
				
		progress_callback.emit(['Generate epub {}'.format(getify.generate_name(novel, data_novel['autor'], 'ch-', book, 1, len(file_list))), 90])
		getify.generate(file_list, novel, data_novel['autor'], 'ch-', book, 1, len(file_list))
	else:
		if export_mode == 0:
			bookList = sorted(data_novel['books'])
			step = 90 / len(bookList)
			pos = 5
			for tome in bookList:
				pos += step
				progress_callback.emit(['generating {} => cover'.format(tome), pos])
				bulk_list = []
				msg1 = tome
				
				getify.cover_generator(data_novel['cover'], novel, tome, data_novel['autor'])
				for bok in data_novel['books'][tome]:
					bulk_list.append(bok)
				file_list = []
				
				for x in range(len(bulk_list)):
					progress_callback.emit(['generating {} => {}'.format(tome, bulk_list[x]['name']), pos])
					ti = bulk_list[x]['url'].split('/')
					filename = "./tmp/"+ti[len(ti) - 1] + ".xhtml"
					filenameOut = "./tmp/"+'ch-{}'.format(x+1)
					try:
						getify.download('https://www.wuxiaworld.com' + bulk_list[x]['url'], filename)
					except HTTPError as e:
						# Return code error (e.g. 404, 501, ...)
						print('URL: {}, HTTPError: {} - {}'.format(bulk_list[x]['url'], e.code, e.reason))
					except URLError as e:
						# Not an HTTP-specific error (e.g. connection refused)
						print('URL: {}, URLError: {}'.format(bulk_list[x]['url'], e.reason))
					else:
						getify.clean(filename, filenameOut, novel)
						file_list.append(filenameOut + ".xhtml")
				progress_callback.emit(['generating {} => {}'.format(tome, getify.generate_name(novel, data_novel['autor'], 'ch-', tome, None, None)), pos])
				getify.generate(file_list, novel, data_novel['autor'], 'ch-', tome, None, None)
		else:#Mode Alternatif
			step = 90 / len(data_novel['alt_books'])
			pos = 5
			for block in data_novel['alt_books']:
				pos += step
				progress_callback.emit(['generating {} => cover'.format(block['title']), pos])
				bulk_list = []
				file_list = []
				getify.cover_generator(data_novel['cover'], novel, block['title'], data_novel['autor'])
				for bl in block['chapters']:
					good = True
					bulk_list.append(bl)
				for x in range(len(bulk_list)):
					progress_callback.emit(['generating {} => {}'.format(block['title'], bulk_list[x]['name']), pos])
					ti = bulk_list[x]['url'].split('/')
					filename = "./tmp/"+ti[len(ti) - 1] + ".xhtml"
					filenameOut = "./tmp/"+'ch-{}'.format(x+1)
					try:
						getify.download('https://www.wuxiaworld.com' + bulk_list[x]['url'], filename)
					except HTTPError as e:
						# Return code error (e.g. 404, 501, ...)
						print('URL: {}, HTTPError: {} - {}'.format(bulk_list[x]['url'], e.code, e.reason))
					except URLError as e:
						# Not an HTTP-specific error (e.g. connection refused)
						print('URL: {}, URLError: {}'.format(bulk_list[x]['url'], e.reason))
					else:
						getify.clean(filename, filenameOut, novel)
						file_list.append(filenameOut + ".xhtml")
				progress_callback.emit(['generating {} => {}'.format(block['title'], getify.generate_name(novel, data_novel['autor'], 'ch-', block['title'], None, None)), pos])
				getify.generate(file_list, novel, data_novel['autor'], 'ch-', block['title'], None, None)
	
def generate_end():
	global dialog, app, novel, cursor, data_novel, generating
	status = "Task finished at {}".format(time.asctime())
	updateStatus(status, True)
	print(status)
	dialog.statusProgressBar.setProperty("value", 100)
	unlockInterface()
	book = dialog.bookSelector.currentText()
	if dialog.totalExportSlider.value() == 0:
		if book != 'Book 0':
			dialog.bookSelector.setEnabled(True)
		dialog.startingChapterSelector.setEnabled(True)
		dialog.endingChapterSelector.setEnabled(True)
	else:
		dialog.bookSelector.setEnabled(True)
		dialog.startingChapterSelector.setEnabled(True)
		dialog.endingChapterSelector.setEnabled(True)
	generating = False
	app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
	subprocess.Popen('explorer "' + os.path.dirname(os.path.realpath(__file__)) + os.sep + 'export' + '"')

def clean_folder(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			#elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)

class MyWindow(QtGui.QMainWindow):
	def closeEvent(self,event):
		global generating
		event.ignore()
		if generating is True: return
		result = QtGui.QMessageBox.question(self, "Confirm Exit...", "Are you sure you want to exit ?", QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
		
		if result == QtGui.QMessageBox.Yes:
			event.accept()



if __name__ == '__main__':
	threadpool = QtCore.QThreadPool()
	myappid = 'wuxiaworld.epubcreator.qt4.2' # arbitrary string
	if os.name == 'nt': ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
	app = QtGui.QApplication([])
	
	
	dir = os.path.dirname(os.path.realpath(__file__))
	app_icon = QtGui.QIcon()
	app_icon.addFile(dir+'/ressources/icon16x16.png', QtCore.QSize(16,16))
	app_icon.addFile(dir+'/ressources/icon24x24.png', QtCore.QSize(24,24))
	app_icon.addFile(dir+'/ressources/icon32x32.png', QtCore.QSize(32,32))
	app_icon.addFile(dir+'/ressources/icon48x48.png', QtCore.QSize(48,48))
	app_icon.addFile(dir+'/ressources/icon256x256.png', QtCore.QSize(256,256))
	app.setWindowIcon(app_icon)
	dialog = interface.Ui_MainWindow()
	window = MyWindow()
	window.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint)
	dialog.setupUi(window)
	window.show()
	
	if 'noupdate' not in sys.argv:
		clean_folder(dir+os.sep+'tmp')
		check_database()
		check_script_version()
	else:
		print('Script in no update mode')
		check_database_final()
	
	fontsList = []
	fontindex = 0
	fontmax = 0
	curFont = ''
	try:
		file1  = open("./ressources/loading_fonts.txt", "r")
		curFont = file1.read()
		file1.close()
		for x in os.listdir('./ressources/fonts'):
			if os.path.isdir('./ressources/fonts/'+x): 
				fontsList.append(x)
				if x == curFont:
					fontindex = fontmax
				fontmax += 1
	except: 
		traceback.print_exc()
		
	
	#set values
	updateStatus('')
	
	dialog.fontSelector.clear()
	dialog.fontSelector.addItems(fontsList)
	dialog.fontSelector.setCurrentIndex(fontindex)
	changeFont()
	
	#set signals/slots
	dialog.exitButton.clicked.connect(exitWindow)
	dialog.novelSelector.currentIndexChanged.connect(changeNovel)
	dialog.fontSelector.currentIndexChanged.connect(changeFont)
	dialog.modeSlider.valueChanged.connect(export_mode_change)
	dialog.totalExportSlider.valueChanged.connect(export_mode_change)
	dialog.bookSelector.currentIndexChanged.connect(book_change)
	dialog.previewButton.clicked.connect(preview)
	dialog.generateButton.clicked.connect(generate)
	
	dialog.generateButton.clicked.connect(generate)
	
	sys.exit(app.exec_())
