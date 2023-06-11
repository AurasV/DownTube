import PySimpleGUI as sg
import yt_dlp


def gui():
    sg.theme('DarkTanBlue')
    layout = [
        [sg.Text('Youtube Link here:')],
        [sg.Input(key='_Link_')],
        [sg.Button('Download', key='_download_'), sg.Button('Exit')],
    ]

    window = sg.Window("Simple YT Downloader", layout)

    while True:
        event, values = window.read()
        print(event, values)

        if event in (None, "Exit"):
            break

        if event == '_download_':
            url = values['_Link_']

            with yt_dlp.YoutubeDL({'format': 'mp4'}) as ydl:
                ydl.download(url)

        window.close()


if __name__ == '__main__':
    gui()