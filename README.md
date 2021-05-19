# GUI_for_image_agreement


### 紀欽益 Chin-Yi Ji

#### Version

- 2021 0519  ver1.0.0 : 上傳 
---
[Introduction](#Intorduction)
[Requirment](#Requirment)
[WithoutPython(.exe)](#WithoutPython(.exe))

[Resource](#Resource)
[Other](#Other)


## Intorduction

1.A GUI for agreement test, which is for checking the consistency of within subjects or between subjects to images.
2.Currently, this program is used sepcific to png files.
3.The GUI is made by PySimpleGUI.

---

## Requirment
```
conda install PySimpleGUI, pandas, pillow
```

Specific version
```
PySimpleGUI== 4.41.2
pandas== 1.1.5
pillow==8.0.0
```

---
## Demo
in cmd or Teminal
 ```cmd
python Agreement_gui_v4.py
```
![image](https://user-images.githubusercontent.com/71117874/118778417-a7973880-b8bc-11eb-9fe0-30498558e36f.png)



---

## WithoutPython(.exe)
You can use pyinstaller to package the program in to a .exe, which can run in a non-pyhton environment such as Windows
First of all, install the pyinstaller package

```
conda install pyinstaller
pip install pyinstaller
```
Direct your Terminal or cmd to the path which Agreement_gui_v4.py is in there.
Then...
```
pyinstaller -wF Agreement_gui_v4.py
```

We will get 3 folder and 1 file in the path,
which is __pycache__, build, dist and Agreement_gui_v4.spec
The .exe file is in the 'dist' folder
![image](https://user-images.githubusercontent.com/71117874/118782240-7caee380-b8c0-11eb-80a2-76feeb8de415.png)

Double click to run the program!!!!(It takes for a while,please be patient~)


## Other



---

