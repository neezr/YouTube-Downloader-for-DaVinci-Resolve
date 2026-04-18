# YouTube Downloader
Download and import YouTube videos to DaVinci Resolve immediately.

You can keep editing while your download is running!

![YouTubeDownloader](https://github.com/neezr/YouTube-Downloader-for-DaVinci-Resolve/assets/145998491/420f6616-6285-4c1d-a276-603cb6c9cb36)

## Usage:
- Run this script from DaVinci Resolve's dropdown menu (```Workspace > Scripts```)
- Select your project folder and paste a YouTube URL into the text field
- The video will automatically be downloaded as .mp4-file with the highest available resolution, placed in your project folder and imported to your Media Pool

## Install:
- Download the file [```YouTube Downloader.py```](YouTube%20Downloader.py)
- Save the file in the *Scripts* folder of DaVinci Resolve:
  - On Windows: ```C:\Users\<YOUR_NAME>\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Utility```
  - On MacOS: ```/Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility```
  - On Linux: ```/opt/resolve/Fusion/Scripts/Utility```


- Install Python (at least version 3.7) from [python.org](https://python.org/)
- Install the python module ```pytube```
	- open ```cmd``` on Windows and execute ```pip install pytube``` in the command line
	- or: install via [```requirements.txt```](requirements.txt) with ```pip install -r requirements.txt```
