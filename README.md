# ~ YouTube Downloader ~
Download and import YouTube videos to DaVinci Resolve immediately.

You can keep editing while your download is running!

![YouTubeDownloader](https://github.com/neezr/YouTube-Downloader-for-DaVinci-Resolve/assets/145998491/420f6616-6285-4c1d-a276-603cb6c9cb36)

## Usage:
- Run this script from DaVinci Resolve's dropdown menu (Workspace > Scripts)
- Select your project folder and paste a YouTube URL into the text field
- The video will automatically be downloaded as .mp4-file with the highest available resolution, placed in your project folder and imported to your Media Pool

## Install:
- Copy the .py-file into the folder "%appdata%\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility"
- Install Python 3.7+
- Install the python modules 'pytube' and 'emoji'
	- open 'cmd' on Windows and execute 'pip install pytube emoji' in the command line
	- or: install via requirements.txt with 'pip install -r requirements.txt'
