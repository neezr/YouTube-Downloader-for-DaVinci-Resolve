#~ YouTube Downloader ~
#created by nizar / version 1.1
#contact: http://twitter.com/nizarneezR

#Usage:
#Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
#Select your project folder and paste a YouTube URL into the text field
#The video will automatically be downloaded as .mp4-file with the highest available resolution, placed in your project folder and imported to your Media Pool

#Install:
#Copy this .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
#Install the python module 'pytube'
#	open cmd and execute 'pip install pytube' in the command line
#	or: install via requirements.txt with 'pip install -r requirements.txt'

import os, tkinter, re
import platform
from tkinter import *
from tkinter import filedialog
from collections import Counter

try:
	from pytube import YouTube, Playlist
except ModuleNotFoundError:
	root_errormsg = Tk()
	root_errormsg.wm_title("Nizar's YouTube Downloader for DaVinci Resolve")
	l_err_msg = Label(root_errormsg, text="Module 'pytube' not found!\n\n'YouTube Downloader' requires the external module 'pytube' for downloading YouTube videos.\nPlease install pytube by opening the command line interface and running 'pip install pytube'.")
	l_err_msg.pack(side="top", fill="x", pady=10)
	l_ok_button = Button(root_errormsg, text="Okay", command=root_errormsg.destroy)
	root_errormsg.mainloop()


def guess_project_folder():
	mp = resolve.GetProjectManager().GetCurrentProject().GetMediaPool()
	filepaths = []
	for mp_item in mp.GetRootFolder().GetClipList():
		try:
			dir_path = os.path.dirname(mp_item.GetClipProperty("File Path"))
			filepaths.append(dir_path)
		except KeyError:
			pass
	
	while "" in filepaths:
		filepaths.remove("")
	
	if not filepaths:
		return None
	else:
		return Counter(filepaths).most_common(1)[0][0]


STANDARD_FILE_LOCATION = guess_project_folder() or {"Windows":os.path.expandvars(r"%APPDATA%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility\YouTube Downloader"),"Darwin":r"/Library/Application Support/Blackmagic Design/Fusion/Scripts/Utility/YouTube Downloader","Linux":r"/opt/resolve/Fusion/Scripts/Utility/YouTube Downloader"}.get(platform.system(), r"/opt/resolve/Fusion/Scripts/Utility/YouTube Downloader")

filelocation = STANDARD_FILE_LOCATION


def downloadVideo(link):
	if link == "":
		pass
	else:
		yt = YouTube(link).streams.get_highest_resolution()
		filename = remove_emoji(yt.default_filename).strip()

		while " ." in filename: #remove trailing white spaces if last characters in title were emojis
			filename = filename.replace(" .", ".")

		print(f"Downloading {filename}...")


		try:
			yt.download(filelocation,filename=filename)
		except:
			print(f"Error: Could not download video at {link}")


		print(f"Done! Downloaded {filename} to {filelocation}")


		resolve.GetMediaStorage().AddItemsToMediaPool(os.path.join(filelocation, filename))

def downloadPlaylist(link):
	if link == "":
		pass
	else:
		playlist = Playlist(link)
		print(f"Downloading playlist: {playlist.title}...")
		for vidurl in playlist.video_urls:
			downloadVideo(vidurl)
		print(f"Done! Downloaded playlist {playlist.title} to {filelocation}")

def download_from_link(link):
	"""
	Decide if this is a video download or playlist download
	"""
	if "/playlist" in link and "PL" in link: # youtube.com/playlist?list=PL.*
		downloadPlaylist(link)
	else: # youtube.com/watch?v=.*(&list=PL.*)? or youtu.be/.*
		downloadVideo(link)
	os.startfile(filelocation, operation="explore")

def remove_emoji(string): #from https://gist.github.com/n1n9-jp/5857d7725f3b14cbc8ec3e878e4307ce
	emoji_patterns = re.compile("["
		u"\U00002700-\U000027BF"  # Dingbats
		u"\U0001F600-\U0001F64F"  # Emoticons
		u"\U00002600-\U000026FF"  # Miscellaneous Symbols
		u"\U0001F300-\U0001F5FF"  # Miscellaneous Symbols And Pictographs
		u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
		u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
		u"\U0001F680-\U0001F6FF"  # Transport and Map Symbols
		"]+", re.UNICODE)
	return re.sub(emoji_patterns, '', string)

#GUI

def gui_download_event():
	global l_entryField, l_downloadbutton
	url = l_entryField.get()
	if len(url) > 0:
		l_downloadbutton.configure(state=DISABLED, text="Downloading...")
		l_entryField.configure(state=DISABLED)
		try:
			download_from_link(url)
		except Exception: #RegexMatchError in pytube
			pass
		l_downloadbutton.configure(state=NORMAL, text="Download")
		l_entryField.configure(state=NORMAL)
		l_entryField.delete(0, END)


def gui_change_filelocation_event():
	global l_filelocation_label, filelocation
	previous_filelocation = filelocation #resetting after canceling out the prompt window
	filelocation = filedialog.askdirectory()
	if not filelocation:
		filelocation = previous_filelocation
	l_filelocation_label.configure(text=filelocation)

def gui_reset_filelocation_event():
	global l_filelocation_label, filelocation, STANDARD_FILE_LOCATION
	filelocation = STANDARD_FILE_LOCATION
	l_filelocation_label.configure(text=filelocation)


root = Tk()
root.title("Nizar's YouTube Downloader for DaVinci Resolve")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
root.configure(background=BG_COLOR)


l_text = Label(root, text="Enter YouTube URL:", bg=BG_COLOR, fg=FG_COLOR)
l_text.grid(row=0, column=0, sticky="W", padx=20, pady=10)
l_entryField = Entry(root, width=50)
l_entryField.grid(row=1,column=0, sticky="W", padx=20)
l_downloadbutton = Button(root, text="Download", padx=50, command=gui_download_event)
l_downloadbutton.grid(row=2, column=0, sticky="W", padx=20, pady=10)


l_filelocation_label = Label(root, text=filelocation, anchor="w", bg=BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg=FG_COLOR)
l_filelocation_label.grid(row=4,column=0, sticky="W", padx=20, pady=(60,10))
l_filelocation_button = Button(root, text="Change download folder", padx=50, command=gui_change_filelocation_event)
l_filelocation_button.grid(row=5,column=0, sticky="W", padx=20)
l_filereset_button = Button(root, text="Reset download folder", padx=50, command=gui_reset_filelocation_event)
l_filereset_button.grid(row=5, column=1, sticky="W", padx=20)


root.mainloop()
