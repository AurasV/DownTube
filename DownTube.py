import PySimpleGUI as sg
import yt_dlp


def gui():
    sg.theme('DarkTanBlue')
    layout = [
        [sg.Text('YouTube link here:')],
        [sg.Input(key='link')],
        [sg.Radio('Video + Audio', 'Type', key='type', default=True),
         sg.Radio('Audio Only', 'Type', key='type'),
         sg.Checkbox('Whole Playlist?', False, key='playlist')],
        [sg.Combo(['2160', '1440', '1080', '720', '480', '360', '240', '144'], default_value='1080',
                  key='resolution'),
         sg.Text('Next highest if not available')],
        [sg.Button('Download', key='download'), sg.Button('Exit')],

    ]

    window = sg.Window("YT Downloader", layout)

    while True:
        event, values = window.read()

        if event in (None, "Exit"):
            break

        if event == 'download':
            if not values['playlist']:
                url = values['link'].split('&list=')[0]

            resolution = values['resolution']
            vid_type = values['type']
            if vid_type:
                options = {
                    'format': f'bestvideo[height<={resolution}][ext=mp4]+bestaudio[ext=m4a]',
                }
            else:
                options = {
                    'format': 'bestaudio[ext=m4a]',
                }
            with yt_dlp.YoutubeDL(options) as ydl:
                try:
                    ydl.download([url])
                    sg.popup('Finished Downloading')
                except yt_dlp.utils.DownloadError:
                    sg.popup("Wrong Link!")

    window.close()


if __name__ == '__main__':
    gui()
