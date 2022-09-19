#stealer app

from pytube import YouTube
from sys import argv
import PySimpleGUI as sg
import os.path
from os.path import exists
import random 

# user can set up default path for ease in future usage if they'd like
# if they don't set up that file, just uses none
try:
    from default_folder import default_path
    disable_run_on_start = False
except:
    default_path = None
    disable_run_on_start = True

# calculate progress each update call
def on_progress(stream, chunk, bytes_remaining):   
    # calculate
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = bytes_downloaded / total_size * 100
    
    # update progress
    window['progText'].update(str(percentage_of_completion) + '%')
    window['progbar'].update(percentage_of_completion)

# called on DL completion
def complete_callback(stream, file_handle):
    window['progbar'].update(100)
    window['progText'].update('100%')
    
    
# Add a touch of color
sg.theme('DarkPurple1') 
  
# var to hold our choice - default to audio
audio_or_video = 'Audio'

# All the stuff inside your window.
layout = [  [
                sg.Text("please don't use this app for stealing")
            ],
            [
                sg.Text('enter a youtube link'), 
                sg.InputText(), 
                sg.Combo(['Audio','Video'], default_value='Audio', enable_events=True, key='comboBox')
            ],           
            [
                sg.Text("Choose a folder: "), 
                sg.Input(key="folder" ,change_submits=True, disabled=True,default_text=default_path),
                sg.FolderBrowse(key="-IN-",initial_folder=default_path)
            ],
            [
                sg.Button('steal anyway',disabled=disable_run_on_start),
                sg.Button('Cancel')
            ],          
            [
                sg.ProgressBar(100, orientation='h', border_width=4, key='progbar',bar_color=['Purple','Green']),
                sg.Text('0%', key='progText'), 
            ]
        ]

window = sg.Window("sols stealer app", layout)

while True:
    event, values = window.read()
       
    # enable run button when folder path is populated
    # leaving case of user leaving blank url - no errors
    if (values and values["folder"]):
        window['steal anyway'].update(disabled=False)     
    
    # get user choice for mp3/4 from comboBox
    if (event == 'comboBox'):        
        audio_or_video = values['comboBox']
        
    # run our process    
    if (event == "steal anyway"):
        # locks up UI but might fix
        
        # reset progress (if any from last run)
        window['progText'].update('0%')
        window['progbar'].update(0)        
        
        # check if we have values first, if user just closes app then values=None and errors out
        if(values[0]):
        
            # grab URL
            link = values[0]
            
            # progress bar goes too quick, so give small manual updates here and there
            #random_number = random.randint(15, 30)
            #window['progText'].update(str(random_number) + '%')
            #window['progbar'].update(random_number)
                                   
            # setup yt object and callbacks for progress updates
            yt = YouTube(link)
            yt.register_on_progress_callback(on_progress)
            yt.register_on_complete_callback(complete_callback)
                                  
            # setup path to save to    
            destination = values['folder'] 
            if not os.path.exists(destination + "\\temp"):                
                os.makedirs(destination)
            
            # save to temp folder so we can check against other files after DL
            destination = destination + "\\temp"
                
            # grab either mp3 or mp4
            if(audio_or_video == 'Audio'):
                ## audio only - grab first available one and download
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=destination) 
            else:              
                ## video (and audio - progressive=True param)
                # wow this is shamefully bad but ok it works 
                # attempts 1 by 1 to to download highest quality b/c Youtube.get_highest_resolution() doesn't actually give me that?? :c
                # might be related - https://github.com/pytube/pytube/issues/194
                video = yt.streams.filter(res="1440p",file_extension='mp4',progressive=True).first()                
                if(video):                    
                    out_file = video.download(output_path=destination)
                else:    
                    video = yt.streams.filter(res="1080p",file_extension='mp4',progressive=True).first()                    
                    if(video):   
                        out_file = video.download(output_path=destination) 
                    else:                
                        video = yt.streams.filter(res="720p",file_extension='mp4',progressive=True).first()                        
                        if(video):                            
                            out_file = video.download(output_path=destination)
                        else:
                            video = yt.streams.filter(res="480p",file_extension='mp4',progressive=True).first()                            
                            if(video):                                
                                out_file = video.download(output_path=destination)            
                            else: 
                                video = yt.streams.first()                                
                                out_file = video.download(output_path=destination)          
            
            # save the file as correct type
            base, ext = os.path.splitext(out_file)
            
            # make new file location one directory back by removing temp folder
            new_file = base.replace('\\temp\\', '\\') + ('_audio.mp3' if audio_or_video == 'Audio' else '_video.mp4')      
            
            # if we don't already have this, add
            if(not exists(new_file)): 
                os.replace(out_file, new_file)
            # if we do have this, just delete from temp
            else:
                os.remove(out_file)
                  
    # close program
    if (event == sg.WIN_CLOSED or event == 'Cancel'):      
        window.close() 
        break