#!/usr/bin/env python
# coding: utf-8

# In[1]:

#Using PySimpleGUI to create GUI
import PySimpleGUI as sg
import os
from pandas import DataFrame
from PIL import Image,ImageTk


# In[2]:

#Get image data using PIL
def get_img_data(f, maxsize=(720, int(720/1.33)), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
  
    return ImageTk.PhotoImage(img)



#file_browser and listbox on the left
file_list_column = [
    [   sg.Text("Enter your name here:",font=('Ariel 16 bold')),
        sg.In(size=(20, 10),font=('Ariel 16'),enable_events=True, key="-DOCTOR-"),       
    ],
    
    [   sg.Text("Image Folder",font=('Ariel 16 bold')),
        sg.In(size=(20, 10),font=('Ariel 14 bold'),enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse('Browse',size=(10,1),button_color='black',font=('Ariel 18 bold')),
    ],
   
    
    [       sg.Listbox(
            values=[], enable_events=True, size=(50, 40),font=('Ariel 14'), key="-FILE LIST-")
    ],
]

#Image and buttons on the right
w,h = sg.Window.get_screen_size() # get the window size

image_viewer_column = [
    [sg.Text("Curret_image_path:",size = (60,1),font=('Ariel 14 bold'))],                               # current path
    [sg.Text(size=(80, 1),font=('Ariel 12 bold'), key="-TOUT-")],                                       # current path
    [sg.Text("Your coded opinion:", text_color = 'black', font=('Ariel 14 bold')),                      # Opinion(Agree or not)
     sg.Text(size=(30, 1),font=('Ariel 14 bold underline'), text_color = 'black',  key="-OPINION-")],   # Opinion(Agree or not)
    [sg.Image(key="-IMAGE-")],                                                                          # Image
    [sg.Button('Agree',size=(10,1),button_color='green',font=('Ariel 20 bold'),pad=(60,3)),             #Buttons
     sg.Button('NotAgree',size=(10,1),button_color='red',font=('Ariel 20 bold'),pad=(80,3)),            #Buttons
     sg.Button('Save',size=(8,1),button_color='grey',font=('Ariel 20 bold')),                           #Buttons
     sg.Button('Close',size=(8,1),button_color='silver',font=('Ariel 20 bold'))],                       #Buttons
   
    
]

# set the layout of the window
layout = [
    [
        sg.Column(file_list_column),    #input_name,browser,listbox
        sg.VSeperator(),                #Divider
        sg.Column(image_viewer_column), #,opinion,Image,button       
    ]
]

#Create a window
w,h = sg.Window.get_screen_size()
window = sg.Window("Agreement on DDH", layout,
                   size=(w,h),location=(20,20),resizable=True,
                   auto_size_text=True,auto_size_buttons=True)

#set current selection index
current_selection_index = 0
#
#button and GUI setting
while True:
    event, values = window.read()      
        
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        global fnames, img_list
        # take png files in the folder to a list
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".PNG"))
        ]
        
        #then create a dataframe to record agreement, all the not-chosen files are coded 0 at first.
        img_list = DataFrame({'File_name':fnames,'Agree':[0]*len(fnames)}) 
        window["-FILE LIST-"].update(fnames)
        
   

    #Click a image file in file list  
    if event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True)) #swith image to the image of clicked file name
            
            opinion = ['Notyetchosen','Agree','NotAgree'] #Three types of Agreement status
            op_now = list(img_list[img_list['File_name']==values["-FILE LIST-"][0]].Agree)[0] #Find the Agreement status of clicked file.
            window["-OPINION-"].update(opinion[op_now]) #update the Agreement status
                        
            #renew the highlight in the list box
            index = fnames.index(values["-FILE LIST-"][0])
            
            current_selection_index = (index)% len(fnames)
            window.Element("-FILE LIST-").update(set_to_index = current_selection_index)
                                             
        except:
            pass
        
    # While pressing Agree or NotAgree
    if event == "Agree" or event == 'NotAgree':
        if event == "Agree":
            img_list['Agree'][img_list.File_name == values["-FILE LIST-"][0]] = 1
        elif event == "NotAgree":  
            img_list['Agree'][img_list.File_name == values["-FILE LIST-"][0]] = 2
        
        try:
            index = fnames.index(values["-FILE LIST-"][0]) #the index of the image file
            
            current_selection_index = (index + 1)% len(fnames)
            
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))
            window.Element('-FILE LIST-').update(set_to_index = current_selection_index)
        except:
            pass
    
    # While pressing 'Close','x',or "Save'
    if event == "Exit" or event == sg.WIN_CLOSED:
        #folder_n = values['-FOLDER-'].replace('/','_') 
        #img_list.to_csv('Not_finished_{}{}.csv'.format(values['-DOCTOR-'],folder_n),index=False)
        break 
    
    if event == "Save":
        #folder_n = values['-FOLDER-'].replace('/','_') 
        img_list.to_csv('{}_agreement.csv'.format(values['-DOCTOR-']),index=False)
        break
        
    if event == "Close":
        #folder_n = values['-FOLDER-'].replace('/','_') 
        img_list.to_csv('Not_finished_{}_agreement.csv'.format(values['-DOCTOR-']),index=False)
        break
        
window.close()
