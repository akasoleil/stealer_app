#stealer app

from pytube import YouTube
from sys import argv
import PySimpleGUI as sg
import os.path


sg.theme('DarkPurple1')   # Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text("please don't use this app for stealing")],
            [sg.Text('enter a youtube link'), sg.InputText()],
            [sg.Text("choose path to steal to")],
            [sg.Text('choose path'), sg.FolderBrowse(key='folder')],
            [sg.Button('steal anyway'), sg.Button('Cancel')] ]

window = sg.Window("sols stealer app", layout)

while True:
    event, values = window.read()
    
    print(values['folder'])

    if event == "steal anyway" or event == sg.WIN_CLOSED or event == 'Cancel':
        break


        


link = values[0]
yt = YouTube(link)
 
print("Title: ", yt.title)

print("View: ", yt.views)

print(values['folder'])

audio = stream = yt.streams.get_by_itag(251)

audio.download(values['folder'])

window.close()
