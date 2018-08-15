#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.14
# In conjunction with Tcl version 8.6
#	Aug 13, 2018 03:57:27 PM

import os
import os.path
import sys
import sqlite3 as sql

try:
	from Tkinter import *
except ImportError:
	from tkinter import *

try:
	import ttk
	py3 = False
except ImportError:
	import tkinter.ttk as ttk
	py3 = True

import interface_support
import novel_data
import database_updator
import getify
from urllib.error import HTTPError, URLError
import time


conn = None
cursor = None

root = None
top = None
novel = ''
data_novel = {}
loop = False

def vp_start_gui():
	'''Starting point when module is the main routine.'''
	global val, w, root, top, conn, cursor
	root = Tk()
	interface_support.set_Tk_var()
	top = New_Toplevel (root)
	interface_support.init(root, top)
	
	if time.time() - float(os.path.getmtime("novels.db")) >= 43200.0: #test 43200 = 12h
		print('Updating Novel Database')
		database_updator.start()
	
	conn = sql.connect("novels.db")
	cursor = conn.cursor()
	cursor.execute("SELECT NovelName,link,autor,cover FROM 'Information'")
	db = cursor.fetchall()
	namelist = []
	for i in db:
		namelist.append(i[0])
		namelist.sort()
	top.TComboboxNovel["values"] = namelist
	top.TComboboxExportMode["values"] = ['Classic', 'Alternative']
	top.TComboboxFullExport["values"] = ['Yes', 'No']
	try: top.TComboboxExportMode.current(0)
	except: {}
	try: top.TComboboxFullExport.current(1)
	except: {}
	
	init_inputs()
	root.mainloop()

w = None
def create_New_Toplevel(root, *args, **kwargs):
	'''Starting point when module is imported by another program.'''
	global w, w_win, rt
	rt = root
	w = Toplevel (root)
	interface_support.set_Tk_var()
	top = New_Toplevel (w)
	interface_support.init(w, top, *args, **kwargs)
	return (w, top)

def destroy_New_Toplevel():
	global w
	w.destroy()
	w = None
		
def init_inputs():
	global top
	top.TComboboxBook["values"] = []
	top.TComboboxStartingChapter["values"] = []
	top.TComboboxEndingChapter["values"] = []
	#top.EntryAltFileName.delete(0, len(top.EntryAltFileName.get()) - 1)
	
	top.TComboboxExportMode.configure(state = "disabled")
	top.TComboboxFullExport.configure(state = "disabled")
	top.TComboboxBook.configure(state = "disabled")
	top.TComboboxStartingChapter.configure(state = "disabled")
	top.TComboboxEndingChapter.configure(state = "disabled")
	#top.EntryAltFileName.configure(state = "disabled")
			
def novel_change(index, value, op):
	global top, novel, cursor, data_novel, root
	
	def callback():
		global top, novel, cursor, data_novel, root
		data_novel['books'], data_novel['alt_books'] = novel_data.import_data(i[0])
		top.TComboboxExportMode.configure(state = "readonly")
		top.TComboboxFullExport.configure(state = "readonly")
		top.LabelStatusBar1.configure(background="#4fa839")
		top.LabelStatusBar1.configure(text='''Novel data loaded''')
		export_mode_change('a', 'b', 'v')
		root.config(cursor="")
	re = top.TComboboxNovel.get()
	export_mode = top.TComboboxExportMode.get()
	export_full = top.TComboboxFullExport.get()
	if novel != re:
		root.config(cursor="wait")
		novel = re
		print(re)
		init_inputs()
		cursor.execute("SELECT link,autor,cover FROM 'Information' WHERE NovelName LIKE ?", (re,))
		db = cursor.fetchall()
		data_novel={}
		for i in db:
			data_novel['link'] = i[0]
			data_novel['autor'] = i[1]
			data_novel['cover'] = i[2]
		root.after(100, callback)
		
def export_mode_change(index, value, op):
	global top, novel, cursor, data_novel
	if 'books' not in data_novel: return
	export_mode = top.TComboboxExportMode.get()
	export_full = top.TComboboxFullExport.get()
	book = top.TComboboxBook.get()
	if export_full == 'No':
		if export_mode == 'Classic':
			if 'Book 01' in data_novel['books']:
				top.TComboboxBook["values"] = sorted(data_novel['books'])
				top.TComboboxBook.configure(state = "readonly")
				try:top.TComboboxBook.current(0)
				except:{}
			else:
				top.TComboboxBook["values"] = ['Book 0']
				top.TComboboxBook.configure(state = "disabled")
				try:top.TComboboxBook.current(0)
				except:{}
			book_change('a', 'b', 'v')
		else:
			books_list = []
			for block in data_novel['alt_books']:
				books_list.append(block['title'])
			top.TComboboxBook["values"] = books_list
			top.TComboboxBook.configure(state = "readonly")
			try:top.TComboboxBook.current(0)
			except:{}
			book_change('a', 'b', 'v')
	else:
		top.TComboboxBook["values"] = []
		top.TComboboxStartingChapter["values"] = []
		top.TComboboxEndingChapter["values"] = []
		#top.EntryAltFileName.delete(0, len(top.EntryAltFileName.get()) - 1)
		
		top.TComboboxBook.configure(state = "disabled")
		top.TComboboxStartingChapter.configure(state = "disabled")
		top.TComboboxEndingChapter.configure(state = "disabled")
		#top.EntryAltFileName.configure(state = "disabled")
		
def book_change(index, value, op):
	global top, novel, cursor, data_novel
	export_mode = top.TComboboxExportMode.get()
	book = top.TComboboxBook.get()
	chapters = []
	if export_mode == 'Classic':
		for bl in data_novel['books'][book]:
			chapters.append(bl['name'])
	else:
		for block in data_novel['alt_books']:
			if block['title'] == book:
				for bl in block['chapters']:
					chapters.append(bl['name'])
					
	top.TComboboxStartingChapter["values"] = chapters
	top.TComboboxEndingChapter["values"] = chapters
	top.TComboboxStartingChapter.current(0)
	top.TComboboxEndingChapter.current(len(chapters) - 1)
	top.TComboboxStartingChapter.configure(state = "readonly")
	top.TComboboxEndingChapter.configure(state = "readonly")
	
def quit():
	global loop
	if loop is True: return
	exit()
	
def generate():
	global top, novel, cursor, data_novel, root, loop
	print('novel: {}'.format(novel))
	if novel == '': return
	
	loop = True
	print('generate_start')
	
	top.TComboboxNovel.configure(state = "disabled")
	top.TComboboxExportMode.configure(state = "disabled")
	top.TComboboxFullExport.configure(state = "disabled")
	top.TComboboxBook.configure(state = "disabled")
	top.TComboboxStartingChapter.configure(state = "disabled")
	top.TComboboxEndingChapter.configure(state = "disabled")
	#top.EntryAltFileName.configure(state = "disabled")
	root.config(cursor="wait")
	
	def callback():
		global top, novel, cursor, data_novel, root, loop
		if novel == '': return
		export_mode = top.TComboboxExportMode.get()
		export_full = top.TComboboxFullExport.get()
		book = top.TComboboxBook.get()
		chapter_start = top.TComboboxStartingChapter.get()
		chapter_end = top.TComboboxEndingChapter.get()
		
		#title = novel
		#data_novel['books'], data_novel['alt_books']
		msg1 = ''
		msg2 = ''
		msg3 = ''
		msg4 = ''
		bulk_list = []
		file_list = []
		if export_full == 'No':
			if export_mode == 'Classic':
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
				print(bulk_list)
					
			msg2 = chapter_start
			msg3 = '=>'
			msg4 = chapter_end
			
			getify.cover_generator(data_novel['cover'], msg1, msg2, msg3, msg4)
			
			for x in range(len(bulk_list)):
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
					
			getify.generate(file_list, novel, data_novel['autor'], 'ch-', book, 1, len(file_list))
		else:
			if export_mode == 'Classic':
				bookList = sorted(data_novel['books'])
				print(bookList)
				for tome in bookList:
					bulk_list = []
					msg1 = tome
					getify.cover_generator(data_novel['cover'], tome, '', '', '')
					for bok in data_novel['books'][tome]:
						bulk_list.append(bok)
					file_list = []
					
					for x in range(len(bulk_list)):
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
					getify.generate(file_list, novel, data_novel['autor'], 'ch-', tome, None, None)
			else:#Mode Alternatif
				for block in data_novel['alt_books']:
					bulk_list = []
					file_list = []
					getify.cover_generator(data_novel['cover'], block['title'], '', '', '')
					for bl in block['chapters']:
						good = True
						bulk_list.append(bl)
					for x in range(len(bulk_list)):
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
					getify.generate(file_list, novel, data_novel['autor'], 'ch-', block['title'], None, None)
		root.after(100, generate_end)
		
	root.after(100, callback)
	
def generate_end():
	global top, novel, cursor, data_novel, root, loop
	print('generate_end')
	top.LabelStatusBar2.configure(text="Task finished{}".format(time.asctime()))
	top.LabelStatusBar2.configure(background="#4fa839")
	book = top.TComboboxBook.get()
	top.TComboboxNovel.configure(state = "readonly")
	top.TComboboxExportMode.configure(state = "readonly")
	top.TComboboxFullExport.configure(state = "readonly")
	if top.TComboboxFullExport.get() == 'No':
		if book != 'Book 0':
			top.TComboboxBook.configure(state = "readonly")
		top.TComboboxStartingChapter.configure(state = "readonly")
		top.TComboboxEndingChapter.configure(state = "readonly")
	else:
		top.TComboboxBook.configure(state = "disabled")
		top.TComboboxStartingChapter.configure(state = "disabled")
		top.TComboboxEndingChapter.configure(state = "disabled")
	root.config(cursor="")
	loop = False

class New_Toplevel:
	def __init__(self, top=None):
		'''This class configures and populates the toplevel window.
		   top is the toplevel containing window.'''
		_bgcolor = '#d9d9d9'  # X11 color: 'gray85'
		_fgcolor = '#000000'  # X11 color: 'black'
		_compcolor = '#d9d9d9' # X11 color: 'gray85'
		_ana1color = '#d9d9d9' # X11 color: 'gray85' 
		_ana2color = '#d9d9d9' # X11 color: 'gray85' 
		self.style = ttk.Style()
		if sys.platform == "win32":
			self.style.theme_use('winnative')
		self.style.configure('.',background=_bgcolor)
		self.style.configure('.',foreground=_fgcolor)
		self.style.configure('.',font="TkDefaultFont")
		self.style.map('.',background=
			[('selected', _compcolor), ('active',_ana2color)])

		top.geometry("595x380+713+237")
		top.title("Wuxiaworld export ebook")
		top.configure(background="#d9d9d9")


		self.LabelNovel = Label(top)
		self.LabelNovel.place(relx=0.02, rely=0.03, height=21, width=174)
		self.LabelNovel.configure(anchor=W)
		self.LabelNovel.configure(background="#a8a8a8")
		self.LabelNovel.configure(disabledforeground="#a3a3a3")
		self.LabelNovel.configure(foreground="#000000")
		self.LabelNovel.configure(justify=LEFT)
		self.LabelNovel.configure(padx="3")
		self.LabelNovel.configure(text='''Select Novel''')
		self.LabelNovel.configure(width=174)

		novel = StringVar()
		novel.trace("w", novel_change)
		self.TComboboxNovel = ttk.Combobox(top)
		self.TComboboxNovel.place(relx=0.32, rely=0.03, relheight=0.06
				, relwidth=0.66)
		self.TComboboxNovel.configure(textvariable=novel)
		self.TComboboxNovel.configure(width=393)
		self.TComboboxNovel.configure(background="#000000")
		self.TComboboxNovel.configure(takefocus="")
		self.TComboboxNovel.configure(state="readonly")

		self.LabelStatusBar1 = Label(top)
		self.LabelStatusBar1.place(relx=0.02, rely=0.11, height=31, width=574)
		self.LabelStatusBar1.configure(activebackground="#f9f9f9")
		self.LabelStatusBar1.configure(activeforeground="black")
		self.LabelStatusBar1.configure(background="#aaaaaa")
		self.LabelStatusBar1.configure(disabledforeground="#a3a3a3")
		self.LabelStatusBar1.configure(foreground="#000000")
		self.LabelStatusBar1.configure(highlightbackground="#d9d9d9")
		self.LabelStatusBar1.configure(highlightcolor="black")
		self.LabelStatusBar1.configure(justify=LEFT)
		self.LabelStatusBar1.configure(padx="3")
		self.LabelStatusBar1.configure(text='''Waiting novel selection''')
		self.LabelStatusBar1.configure(width=574)

		self.LabelExportMode = Label(top)
		self.LabelExportMode.place(relx=0.02, rely=0.21, height=21, width=174)
		self.LabelExportMode.configure(activebackground="#f9f9f9")
		self.LabelExportMode.configure(activeforeground="black")
		self.LabelExportMode.configure(anchor=W)
		self.LabelExportMode.configure(background="#a8a8a8")
		self.LabelExportMode.configure(disabledforeground="#a3a3a3")
		self.LabelExportMode.configure(foreground="#000000")
		self.LabelExportMode.configure(highlightbackground="#d9d9d9")
		self.LabelExportMode.configure(highlightcolor="black")
		self.LabelExportMode.configure(justify=LEFT)
		self.LabelExportMode.configure(padx="3")
		self.LabelExportMode.configure(text='''Select export Mode''')

		exportMode = StringVar()
		exportMode.trace("w", export_mode_change)
		self.TComboboxExportMode = ttk.Combobox(top)
		self.TComboboxExportMode.place(relx=0.32, rely=0.21, relheight=0.06
				, relwidth=0.66)
		self.TComboboxExportMode.configure(textvariable=exportMode)
		self.TComboboxExportMode.configure(width=393)
		self.TComboboxExportMode.configure(takefocus="")
		self.TComboboxExportMode.configure(state="readonly")

		self.LabelFullExport = Label(top)
		self.LabelFullExport.place(relx=0.02, rely=0.29, height=21, width=174)
		self.LabelFullExport.configure(activebackground="#f9f9f9")
		self.LabelFullExport.configure(activeforeground="black")
		self.LabelFullExport.configure(anchor=W)
		self.LabelFullExport.configure(background="#a8a8a8")
		self.LabelFullExport.configure(disabledforeground="#a3a3a3")
		self.LabelFullExport.configure(foreground="#000000")
		self.LabelFullExport.configure(highlightbackground="#d9d9d9")
		self.LabelFullExport.configure(highlightcolor="black")
		self.LabelFullExport.configure(justify=LEFT)
		self.LabelFullExport.configure(padx="3")
		self.LabelFullExport.configure(text='''Full export ?''')

		fullExport = StringVar()
		fullExport.trace("w", export_mode_change)
		self.TComboboxFullExport = ttk.Combobox(top)
		self.TComboboxFullExport.place(relx=0.32, rely=0.29, relheight=0.06
				, relwidth=0.66)
		self.TComboboxFullExport.configure(textvariable=fullExport)
		self.TComboboxFullExport.configure(width=393)
		self.TComboboxFullExport.configure(takefocus="")
		self.TComboboxFullExport.configure(state="readonly")

		self.LabelBook = Label(top)
		self.LabelBook.place(relx=0.02, rely=0.37, height=21, width=174)
		self.LabelBook.configure(activebackground="#f9f9f9")
		self.LabelBook.configure(activeforeground="black")
		self.LabelBook.configure(anchor=W)
		self.LabelBook.configure(background="#a8a8a8")
		self.LabelBook.configure(disabledforeground="#a3a3a3")
		self.LabelBook.configure(foreground="#000000")
		self.LabelBook.configure(highlightbackground="#d9d9d9")
		self.LabelBook.configure(highlightcolor="black")
		self.LabelBook.configure(justify=LEFT)
		self.LabelBook.configure(padx="3")
		self.LabelBook.configure(text='''Select book''')

		book = StringVar()
		book.trace("w", book_change)
		self.TComboboxBook = ttk.Combobox(top)
		self.TComboboxBook.place(relx=0.32, rely=0.37, relheight=0.06
				, relwidth=0.66)
		self.TComboboxBook.configure(textvariable=book)
		self.TComboboxBook.configure(width=393)
		self.TComboboxBook.configure(takefocus="")
		self.TComboboxBook.configure(state="readonly")

		self.LabelStartingChapter = Label(top)
		self.LabelStartingChapter.place(relx=0.02, rely=0.45, height=21, width=174)
		self.LabelStartingChapter.configure(activebackground="#f9f9f9")
		self.LabelStartingChapter.configure(activeforeground="black")
		self.LabelStartingChapter.configure(anchor=W)
		self.LabelStartingChapter.configure(background="#a8a8a8")
		self.LabelStartingChapter.configure(disabledforeground="#a3a3a3")
		self.LabelStartingChapter.configure(foreground="#000000")
		self.LabelStartingChapter.configure(highlightbackground="#d9d9d9")
		self.LabelStartingChapter.configure(highlightcolor="black")
		self.LabelStartingChapter.configure(justify=LEFT)
		self.LabelStartingChapter.configure(padx="3")
		self.LabelStartingChapter.configure(text='''Starting Chapter''')

		startingChapter = StringVar()
		self.TComboboxStartingChapter = ttk.Combobox(top)
		self.TComboboxStartingChapter.place(relx=0.32, rely=0.45, relheight=0.06
				, relwidth=0.66)
		self.TComboboxStartingChapter.configure(textvariable=startingChapter)
		self.TComboboxStartingChapter.configure(width=393)
		self.TComboboxStartingChapter.configure(takefocus="")
		self.TComboboxStartingChapter.configure(state="readonly")

		self.LabelEndingChapter = Label(top)
		self.LabelEndingChapter.place(relx=0.02, rely=0.53, height=21, width=174)
		self.LabelEndingChapter.configure(activebackground="#f9f9f9")
		self.LabelEndingChapter.configure(activeforeground="black")
		self.LabelEndingChapter.configure(anchor=W)
		self.LabelEndingChapter.configure(background="#a8a8a8")
		self.LabelEndingChapter.configure(disabledforeground="#a3a3a3")
		self.LabelEndingChapter.configure(foreground="#000000")
		self.LabelEndingChapter.configure(highlightbackground="#d9d9d9")
		self.LabelEndingChapter.configure(highlightcolor="black")
		self.LabelEndingChapter.configure(justify=LEFT)
		self.LabelEndingChapter.configure(padx="3")
		self.LabelEndingChapter.configure(text='''Ending Chapter''')

		endingChapter = StringVar()
		self.TComboboxEndingChapter = ttk.Combobox(top)
		self.TComboboxEndingChapter.place(relx=0.32, rely=0.53, relheight=0.06
				, relwidth=0.66)
		self.TComboboxEndingChapter.configure(textvariable=endingChapter)
		self.TComboboxEndingChapter.configure(width=393)
		self.TComboboxEndingChapter.configure(takefocus="")
		self.TComboboxEndingChapter.configure(state="readonly")

		
		#self.LabelAltFileName = Label(top)
		#self.LabelAltFileName.place(relx=0.02, rely=0.61, height=21, width=174)
		#self.LabelAltFileName.configure(activebackground="#f9f9f9")
		#self.LabelAltFileName.configure(activeforeground="black")
		#self.LabelAltFileName.configure(anchor=W)
		#self.LabelAltFileName.configure(background="#a8a8a8")
		#self.LabelAltFileName.configure(disabledforeground="#a3a3a3")
		#self.LabelAltFileName.configure(foreground="#000000")
		#self.LabelAltFileName.configure(highlightbackground="#d9d9d9")
		#self.LabelAltFileName.configure(highlightcolor="black")
		#self.LabelAltFileName.configure(justify=LEFT)
		#self.LabelAltFileName.configure(padx="3")
		#self.LabelAltFileName.configure(text='''Alternative file name''')

		#self.EntryAltFileName = Entry(top)
		#self.EntryAltFileName.place(relx=0.32, rely=0.61,height=20, relwidth=0.66)
		#self.EntryAltFileName.configure(background="white")
		#self.EntryAltFileName.configure(disabledforeground="#a3a3a3")
		#self.EntryAltFileName.configure(font="TkFixedFont")
		#self.EntryAltFileName.configure(foreground="#000000")
		#self.EntryAltFileName.configure(insertbackground="black")
		#self.EntryAltFileName.configure(width=394)
		
		
		self.ButtonExit = Button(top)
		self.ButtonExit.place(relx=0.02, rely=0.695, height=24, width=174)
		self.ButtonExit.configure(activebackground="#d80000")
		self.ButtonExit.configure(activeforeground="white")
		self.ButtonExit.configure(activeforeground="#000000")
		self.ButtonExit.configure(background="#d80000")
		self.ButtonExit.configure(disabledforeground="#a3a3a3")
		self.ButtonExit.configure(foreground="#FFFFFF")
		self.ButtonExit.configure(highlightbackground="#d9d9d9")
		self.ButtonExit.configure(highlightcolor="black")
		self.ButtonExit.configure(pady="0")
		self.ButtonExit.configure(text='''Exit''')
		self.ButtonExit.configure(width=170)
		self.ButtonExit.configure(command = quit)

		self.TButtonGenerate = ttk.Button(top)
		self.TButtonGenerate.place(relx=0.32, rely=0.695, height=25, width=392)
		self.TButtonGenerate.configure(takefocus="")
		self.TButtonGenerate.configure(text='''Generate''')
		self.TButtonGenerate.configure(width=396)
		self.TButtonGenerate.configure(command = generate)

		self.LabelStatusBar2 = Label(top)
		self.LabelStatusBar2.place(relx=0.02, rely=0.87, height=31, width=572)
		self.LabelStatusBar2.configure(activebackground="#f9f9f9")
		self.LabelStatusBar2.configure(activeforeground="black")
		self.LabelStatusBar2.configure(background="#aaaaaa")
		self.LabelStatusBar2.configure(disabledforeground="#a3a3a3")
		self.LabelStatusBar2.configure(foreground="#000000")
		self.LabelStatusBar2.configure(highlightbackground="#d9d9d9")
		self.LabelStatusBar2.configure(highlightcolor="black")
		self.LabelStatusBar2.configure(justify=LEFT)
		self.LabelStatusBar2.configure(padx="3")
		self.LabelStatusBar2.configure(text="")
		self.LabelStatusBar2.configure(width=574)


if __name__ == '__main__':
	vp_start_gui()
