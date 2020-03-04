#Hej
import youtube_dl
import ffmpeg
import os
import sys
import os.path
from mega import Mega
from secrets import email, password

if os.path.isfile('/home/pi/MusicDownloader/running.lock'):
    print("Already running, exiting...")
    sys.exit()

f = open("/home/pi/MusicDownloader/running.lock", "x")

files = []

def my_hook(d):
    if d['status'] == 'finished':
        webm = d['filename']
        mp3 = webm.replace('.webm', '.mp3')
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

if not files:
    print('Nothing to upload')
else:
    mega = Mega()
    m = mega.login(email, password)
    print('Logged in to {}'.format(email))

    # Upload to MEGA
    folder = m.find('Port Du Soleil')
    for item in files:
        m.upload(item, folder[0])
        print('{} uploaded!'.format(item))

    print('All files uploaded!')

for item in files:
    os.remove(item)

#os.remove('/home/pi/MusicDownloader/running.lock')