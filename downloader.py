#Hej
import youtube_dl
import ffmpeg
import os
import sys
import os.path
from datetime import datetime
from mega import Mega
from secrets import email, password


if os.path.isfile('/home/pi/MusicDownloader/running.lock'):
    print("Already running, exiting...")
    sys.exit()

lock = open("/home/pi/MusicDownloader/running.lock", "x")
lock.close()

log = open("/home/pi/MusicDownloader/logger.log", "a+")

now = datetime.now()
log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Started...'

files = []

def my_hook(d):
    if d['status'] == 'finished':
        webm = d['filename']
        if 'webm' in webm: 
            mp3 = webm.replace('.webm', '.mp3')

        elif '.m4a' in webm:
            mp3 = webm.replace('.m4a', '.mp3')

        else:
            now = datetime.now()
            log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Could not change filename'
            sys.exit()
        
        files.append(mp3)
        now = datetime.now()
        log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Added {} to list!'.format(mp3))

    if d['status'] == 'downloading':
        now = datetime.now()
        log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Downloading ' + d['filename'])
        

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
    now = datetime.now()
    log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Nothing to upload'
else:
    mega = Mega()
    m = mega.login(email, password)
    now = datetime.now()
    log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Logged in to {}'.format(email))

    # Upload to MEGA
    folder = m.find('FromYoutube')
    for item in files:
        now = datetime.now()
        log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'Uploading {}'.format(item))

        #Actual uploading
        m.upload(item, folder[0])

        now = datetime.now()
        log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + '{} uploaded!'.format(item))

    now = datetime.now()
    log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + 'All files uploaded!')

for item in files:
    os.remove(item)

os.remove('/home/pi/MusicDownloader/running.lock')

now = datetime.now()
log.write(now.strftime("%m-%d-%Y %H:%M:%S - ") + ' --- DONE! ---')
log.close()