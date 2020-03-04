#Hej
import youtube_dl
import ffmpeg
import os
import sys
import os.path
import datetime
from mega import Mega
from secrets import email, password

now = datetime.datetime.now()

print(now.strftime("%Y-%m-%d %H:%M:%S"))

if os.path.isfile('/home/pi/MusicDownloader/running.lock'):
    print("Already running, exiting...")
    sys.exit()

f = open("/home/pi/MusicDownloader/running.lock", "x")

files = []

def my_hook(d):
    if d['status'] == 'finished':
        webm = d['filename']
        if '.mp3' in webm: 
            mp3 = webm.replace('.webm', '.mp3')

        if '.m4a' in webm:
            mp3 = webm.replace('.m4a', '.mp3')
        
        files.append(mp3)
        print('Added {} to list!'.format(mp3))

ydl_opts = {
    'format': 'bestaudio',
    'download_archive': '/home/pi/MusicDownloader/archive.txt',
    'outtmpl': '%(title)s - %(uploader)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '320',
    }],
    'progress_hooks': [my_hook]
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['https://www.youtube.com/playlist?list=PLP_yH_3aruhXVkpN2TIU-jexyunVB-g4P'])

now = datetime.datetime.now()

print(now.strftime("%Y-%m-%d %H:%M:%S"))

if not files:
    print('Nothing to upload')
else:
    mega = Mega()
    m = mega.login(email, password)
    print('Logged in to {}'.format(email))

    # Upload to MEGA
    folder = m.find('Port Du Soleil')
    for item in files:
        print('Uploading {}'.format(item))
        m.upload(item, folder[0])
        print('{} uploaded!'.format(item))

    print('All files uploaded!')

for item in files:
    os.remove(item)

os.remove('/home/pi/MusicDownloader/running.lock')