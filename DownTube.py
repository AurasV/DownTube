import PySimpleGUI as sg
import yt_dlp
import os
import time


def change_time(path):
    new_time = time.time()
    os.utime(path, (new_time, new_time))


def gui():
    sg.theme('DarkTanBlue')
    layout = [
        [sg.Text('YouTube link here:')],
        [sg.Input(key='link')],
        [sg.Radio('Video + Audio', 'Type', key='type', default=True),
         sg.Radio('Audio Only', 'Type', key='type'),
         sg.Checkbox('Whole Playlist?', False, key='playlist')],
        [sg.FolderBrowse('Location', key='downloaddir'), sg.Text('Download Location: Same as Program', size=(31, 1))],
        [sg.Combo(['2160', '1440', '1080', '720', '480', '360', '240', '144'], default_value='1080',
                  key='resolution'),
         sg.Text('Next highest if not available')],
        [sg.Button('Download', key='download'), sg.Button('Exit')],

    ]

    window = sg.Window("DownTube", layout, icon='icon.ico')

    while True:
        event, values = window.read()

        if event in (None, "Exit"):
            break

        if event == 'download':
            dl_playlist = values['playlist']
            if not dl_playlist:
                url = values['link'].split('&list=')[0]
            else:
                url = values['link']
            download_folder = values['downloaddir']
            resolution = values['resolution']
            vid_type = values['type']
            if vid_type:
                extension = '.mp4'
                options = {
                    'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]',
                    'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
                    'ignoreerrors': True,
                }
            else:
                extension = '.m4a'
                options = {
                    'format': 'bestaudio[ext=m4a]',
                    'outtmpl': f'{download_folder}/%(title)s.%(ext)s',
                    'ignoreerrors': True,
                }
            with yt_dlp.YoutubeDL(options) as ydl:
                try:
                    ydl.download(url)
                    if not dl_playlist:
                        vid_info = ydl.extract_info(url, download=False)
                        title = vid_info.get('title') + extension
                        full_path = download_folder + '/' + title
                        change_time(full_path)
                    sg.popup('Download Finished!')
                except yt_dlp.utils.DownloadError:
                    sg.popup("Wrong Link!")

    window.close()


if __name__ == '__main__':
    gui()
