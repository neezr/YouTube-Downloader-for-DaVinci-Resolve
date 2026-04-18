# YouTube Downloader
# created by nizar
# contact: http://twitter.com/nizarneezR

# Usage:
# Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
# Select your project folder and paste a YouTube URL into the text field
# The video will automatically be downloaded as .mp4-file with the highest available resolution, placed in your project folder and imported to your Media Pool

# Install:
# Copy this .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
# Install the python module 'pytubefix'
#    open cmd and execute 'pip install pytubefix' in the command line
#    or: install via requirements.txt with 'pip install -r requirements.txt'

import os
import tkinter
import re
import platform
from collections import Counter
from tkinter import filedialog

DOWNLOAD_DEVICE = "ANDROID_VR"

def show_error_message(msg):
    root_errormsg = tkinter.Tk()
    root_errormsg.wm_title("Nizar's YouTube Downloader for DaVinci Resolve")
    l_err_msg = tkinter.Label(root_errormsg, text=msg)
    l_err_msg.pack(side="top", fill="x", pady=10)
    l_ok_button = tkinter.Button(root_errormsg, text="Okay", command=root_errormsg.destroy)
    root_errormsg.mainloop()

try:
    try:
        from pytubefix import YouTube, Playlist
    except ModuleNotFoundError:
        from pytube import YouTube, Playlist
        print("Imported pytube instead of pytubefix. Expect unresolved issues.")
except ModuleNotFoundError:
    show_error_message("Module 'pytubefix' not found!\n\n'YouTube Downloader' requires the external module 'pytubefix' for downloading YouTube videos.\nPlease install pytubefix by opening the command line interface and running 'pip install pytubefix'.")


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

OS_TO_STANDARD_FILE_LOCATION = {"Windows": os.path.expandvars(r"%USERPROFILE%\Downloads"), "Darwin": os.path.expanduser("~/Downloads"), "Linux": os.path.expanduser("~/Downloads")}
STANDARD_FILE_LOCATION = guess_project_folder() or OS_TO_STANDARD_FILE_LOCATION.get(platform.system(), "Linux")

filelocation = STANDARD_FILE_LOCATION


def download_video(link, audio_only=False):
    if link == "":
        pass
    else:
        if audio_only:
            yt = YouTube(link, client=DOWNLOAD_DEVICE).streams.filter(only_audio=True)[0]
        else:
            yt = YouTube(link, client=DOWNLOAD_DEVICE).streams.get_highest_resolution()
        filename = remove_emoji(yt.default_filename).strip() # ends with .mp4 or .m4a

        filename = re.sub(r" \.", r"\.", filename) #remove trailing white spaces if last characters in title were emojis
        

        print(f"Downloading {filename}...")


        try:
            file_path = yt.download(filelocation,filename=filename)
        except:
            print(f"Error: Could not download video at {link}")


        print(f"Done! Downloaded {file_path}")

        resolve.GetMediaStorage().AddItemListToMediaPool([file_path])

def download_playlist(link, audio_only=False):
    if link == "":
        pass
    else:
        playlist = Playlist(link, client=DOWNLOAD_DEVICE)
        print(f"Downloading playlist: {playlist.title}...")
        for vidurl in playlist.video_urls:
            download_video(vidurl, audio_only)
        print(f"Done! Downloaded playlist {playlist.title} to {filelocation}")

def download_from_link(link, audio_only=False):
    """
    Decide if this is a video download or playlist download
    """
    if "/playlist" in link and "PL" in link: # youtube.com/playlist?list=PL.*
        download_playlist(link, audio_only)
    else: # youtube.com/watch?v=.*(&list=PL.*)? or youtu.be/.*
        download_video(link, audio_only)
    if platform.system() == "Windows":
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
    audio_only = audio_only_var.get()
    if len(url) > 0:
        l_downloadbutton.configure(state=tkinter.DISABLED, text="Downloading...")
        l_entryField.configure(state=tkinter.DISABLED)
        try:
            download_from_link(url, audio_only)
        except Exception as e: # RegexMatchError in pytube or failed download
            show_error_message(f"Error downloading {url}:\n\n{e}\n\nThis error possibly emerged from an update in YouTube's API. In that case, please download a new version of 'YouTube Downloader' from https://github.com/neezr/YouTube-Downloader-for-DaVinci-Resolve/")
        l_downloadbutton.configure(state=tkinter.NORMAL, text="Download")
        l_entryField.configure(state=tkinter.NORMAL)
        l_entryField.delete(0, tkinter.END)


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


root = tkinter.Tk()
root.title("Nizar's YouTube Downloader for DaVinci Resolve")
BG_COLOR = '#28282e'
FG_COLOR = '#cac5c4'
root.configure(background=BG_COLOR)

audio_only_var = tkinter.BooleanVar()

l_text = tkinter.Label(root, text="Enter YouTube URL:", bg=BG_COLOR, fg=FG_COLOR)
l_text.grid(row=0, column=0, sticky="W", padx=20, pady=10)
l_entryField = tkinter.Entry(root, width=50)
l_entryField.grid(row=1,column=0, sticky="W", padx=20)
l_downloadbutton = tkinter.Button(root, text="Download", padx=50, command=gui_download_event)
l_downloadbutton.grid(row=2, column=0, sticky="W", padx=20, pady=10)

l_audio_button = tkinter.Checkbutton(root, text='Audio Only',variable=audio_only_var, onvalue=True, offvalue=False, anchor="w", bg=BG_COLOR, activebackground = BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg="gray")
l_audio_button.grid(row=3, column=1, sticky="W", padx=20, pady=10)

l_filelocation_label = tkinter.Label(root, text=filelocation, anchor="w", bg=BG_COLOR, highlightbackground = "gray", highlightthickness=2, fg=FG_COLOR)
l_filelocation_label.grid(row=4,column=0, sticky="W", padx=20, pady=(60,10))
l_filelocation_button = tkinter.Button(root, text="Change download folder", padx=50, command=gui_change_filelocation_event)
l_filelocation_button.grid(row=5,column=0, sticky="W", padx=20)
l_filereset_button = tkinter.Button(root, text="Reset download folder", padx=50, command=gui_reset_filelocation_event)
l_filereset_button.grid(row=5, column=1, sticky="W", padx=20)


root.mainloop()
