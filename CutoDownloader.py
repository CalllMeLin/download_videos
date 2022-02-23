import urllib.request
import PySimpleGUI as sg
import re
from PIL import Image, ImageTk
from pytube import YouTube

def download():

    for i in range(1,7):
        if event == 'download_button_mp3_'+str(i):
            choose_mp3_or_mp4 = sg.Window(
                'File Options', [
                    [sg.T("What will you name the file? "), sg.I(k="file_name")],
                    [sg.T('What format do you wish to download?')], 

                    [
                        sg.Button('MP3',s=15),
                        sg.Button('MP4',s=15), sg.Button('Cancel',s=15)
                    ]
                ]
                ).read(close=True)

            if choose_mp3_or_mp4[0] == 'MP3':

                url = YouTube( "https://www.youtube.com/watch?v=" + video_ids[i-1] )
                video = url.streams.get_audio_only()
                if(choose_mp3_or_mp4[1] ['file_name']) == '':
                    video.download( filename=(
                        str(video_titles[i-1]).replace(':','').replace('"','').replace('|','') +'.mp3'
                        )
                    )

                else:
                    video.download( filename = (choose_mp3_or_mp4[1] ['file_name']) + '.mp3')  

                sg.popup_ok("Download Complete!")

            elif choose_mp3_or_mp4[0] == 'MP4':

                url = YouTube( "https://www.youtube.com/watch?v=" + video_ids[i-1] )
                video = url.streams.get_highest_resolution()

                if(choose_mp3_or_mp4[1] ['file_name']) == '':
                    video.download( filename=(
                        str(video_titles[i-1]).replace(':','').replace('"','').replace('|','')+".mp4"
                        ) 
                    )

                else:
                    video.download( filename=( choose_mp3_or_mp4[1] ['file_name']) + ".mp4")

                sg.popup_ok("Download Complete!")
                
n_img = 1

video_titles = []

layout = [
    [sg.T("Insert the search parameter: ",pad=(14,0)), sg.I(key='search_input')],
    [sg.B('Search',size=(22,0), pad=(4,7))],
    [sg.T('', k='video_title_1', pad=(1,0))], [sg.Image('', key='img1'), sg.B('Download Video 1', k='download_button_mp3_1',visible=False)],
    [sg.T('', k='video_title_2', pad=(1,0))], [sg.Image('', key='img2'), sg.B('Download Video 2', k='download_button_mp3_2',visible=False)],
    [sg.T('', k='video_title_3', pad=(1,0))], [sg.Image('', key='img3'), sg.B('Download Video 3', k='download_button_mp3_3',visible=False)],
    [sg.T('', k='video_title_4', pad=(1,0))], [sg.Image('', key='img4'), sg.B('Download Video 4', k='download_button_mp3_4',visible=False)],
    [sg.T('', k='video_title_5', pad=(1,0))], [sg.Image('', key='img5'), sg.B('Download Video 5', k='download_button_mp3_5',visible=False)],
    [sg.T('', k='video_title_6', pad=(1,0))], [sg.Image('', key='img6'), sg.B('Download Video 6', k='download_button_mp3_6',visible=False)]
]

window = sg.Window("Cuto Downloader",layout,finalize=True,size=(650,700),resizable=True)

while True:
    
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        
        break
    
    if event == 'Search':

        values['search_input'] = "https://www.youtube.com/results?search_query="+values['search_input'].replace(' ','+')
        link = urllib.request.urlopen(values['search_input'])
        video_ids = re.findall(r"watch\?v=(\S{11})", link.read().decode())

        del video_ids[6:] 
        #Deleting a bunch of videos from the result, I want the max number of results to be 6

        #Showing the thumbnail of each video vvvv

        for index in video_ids:
            urllib.request.urlretrieve(
                f"https://i.ytimg.com/vi/{index}/hqdefault.jpg?sqp=-oaymwEbCKgBEF5IVfKriqkDDggBFQAAiEIYAXABwAEG&rs=AOn4CLCS6cs4L97xxnXYTOVP7q7CMrN0Gw",
                f'thumb_{n_img}.png'
                )
            yot = YouTube("https://www.youtube.com/watch?v=" + index)
            video_titles.append(yot.title)
            window[f'video_title_{n_img}'].update(yot.title)
            img_thumb = Image.open(f'thumb_{n_img}.png')
            img_thumb = img_thumb.resize((180,80))
            window[f'download_button_mp3_{n_img}'].update(visible=True)
            window[f'img{n_img}'].update(data=ImageTk.PhotoImage(image=img_thumb))
            n_img+=1
    n_img = 1
    download()
