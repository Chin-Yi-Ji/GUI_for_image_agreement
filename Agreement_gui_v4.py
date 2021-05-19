#!/usr/bin/env python
# coding: utf-8

# In[1]:


import PySimpleGUI as sg
import os
from pandas import DataFrame
from PIL import Image,ImageTk


# In[2]:


def get_img_data(f, maxsize=(720, int(720/1.33)), first=False):
    """Generate image data using PIL
    """
    img = Image.open(f)
    img.thumbnail(maxsize)
  
    return ImageTk.PhotoImage(img)



#左邊的file_browser和listbox
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
#右邊的圖像以及按鈕視窗
w,h = sg.Window.get_screen_size()

image_viewer_column = [
    [sg.Text("Curret_image_path:",size = (60,1),font=('Ariel 14 bold'))],
    [sg.Text(size=(80, 1),font=('Ariel 12 bold'), key="-TOUT-")],    
    [sg.Text("Your coded opinion:", text_color = 'black', font=('Ariel 14 bold')),
     sg.Text(size=(30, 1),font=('Ariel 14 bold underline'), text_color = 'black',  key="-OPINION-")],    
    [sg.Image(key="-IMAGE-")],
    [sg.Button('Agree',size=(10,1),button_color='green',font=('Ariel 20 bold'),pad=(60,3)),
     sg.Button('NotAgree',size=(10,1),button_color='red',font=('Ariel 20 bold'),pad=(80,3)),
     sg.Button('Save',size=(8,1),button_color='grey',font=('Ariel 20 bold')),
     sg.Button('Close',size=(8,1),button_color='silver',font=('Ariel 20 bold'))],
   
    
]

#把畫面結構抓出來
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),        
    ]
]

#建立視窗
w,h = sg.Window.get_screen_size()
window = sg.Window("Agreement on DDH", layout,
                   size=(w,h),location=(20,20),resizable=True,
                   auto_size_text=True,auto_size_buttons=True)

#set current selection index
current_selection_index = 0
#

while True:
    event, values = window.read()      
        
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            file_list = os.listdir(folder)
        except:
            file_list = []
        global fnames, img_list
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".png", ".PNG"))
        ]
        img_list = DataFrame({'File_name':fnames,'Agree':[0]*len(fnames)})
        window["-FILE LIST-"].update(fnames)
        
   

    ##點選File list中的一個
  
    if event == "-FILE LIST-":
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))
            
            opinion = ['Unread','Agree','NotAgree']
            op_now = list(img_list[img_list['File_name']==values["-FILE LIST-"][0]].Agree)[0]
            window["-OPINION-"].update(opinion[op_now])
            
            
            #更新listbox的反黑部份
            index = fnames.index(values["-FILE LIST-"][0])
            
            current_selection_index = (index)% len(fnames)
            window.Element("-FILE LIST-").update(set_to_index = current_selection_index)
            
           
                        
        except:
            pass
        
    ##按下Agree or NotAgree
    if event == "Agree" or event == 'NotAgree':
        if event == "Agree":
            img_list['Agree'][img_list.File_name == values["-FILE LIST-"][0]] = 1
        elif event == "NotAgree":  
            img_list['Agree'][img_list.File_name == values["-FILE LIST-"][0]] = 2
        
        try:
            index = fnames.index(values["-FILE LIST-"][0])
            
            current_selection_index = (index + 1)% len(fnames)
            
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TOUT-"].update(filename)
            window["-IMAGE-"].update(data=get_img_data(filename, first=True))
            window.Element('-FILE LIST-').update(set_to_index = current_selection_index)
        except:
            pass
    
    #如果按了離開或關閉
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


# In[5]:


int(200/1.33)


# In[8]:


aa=DataFrame({'allwa':[1,2,3],'nono':[4,5,6]})


# In[13]:


aa[aa.allwa==1].nono=-1


# In[14]:


aa


# In[ ]:




