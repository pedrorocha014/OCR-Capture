#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyautogui
import easyocr
import numpy as np
import csv
import os.path

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


# In[2]:


def getText():
    focusBase = screenSizeConfig.get()
    
    x_position = pyautogui.position().x - (focusBase/2)
    y_position = pyautogui.position().y - (focusBase/2)

    myScreenshot = pyautogui.screenshot(region=(x_position,y_position,focusBase,focusBase))
    pix = np.array(myScreenshot)
    
    reader = easyocr.Reader(['pt'])
    
    meta = []
    result = reader.readtext(pix, paragraph=True)
    
    for res in result:
        meta.append([res[1]]) 
    
    return meta

def getKeyDown(event):
    if event.char == 'p':
        text = getText()
        textEntry.delete(0,END)
        textEntry.insert(0,text)
        
def saveText():
    text = textEntry.get()
    category = categoryEntry.get()
    index = textListbox.size() - 1 if textListbox.size() > 0 else 0
    textListbox.insert(index, text + ";" + category)
    
def exportToCsv():
    selectedDir = filedialog.askdirectory()
    fullPath = os.path.join(selectedDir, 'textExport.csv')
    
    arrayData = []
    
    data = textListbox.get(0, END)
    
    for dataText in data:
        arrayData.append([dataText])
    
    with open(fullPath, 'w', encoding='UTF8', newline='') as f:        
        writer = csv.writer(f)
        writer.writerows(arrayData)
        f.close()


# In[40]:


root = Tk()
root.title('OCR Capture')
frm = ttk.Frame(root, padding=10)
tabControl = ttk.Notebook(root)
  
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
  
tabControl.add(tab1, text ='Capture')
tabControl.add(tab2, text ='Configuration')
tabControl.pack(expand = 1, fill ="both")

#TAB 1

choices = ['Tag', 'Valve', 'Line']

Label(tab1, text="Text Value").grid(column=0, row=0, sticky='W')
textEntry = ttk.Entry(tab1)
textEntry.grid(column=1, row=0,pady=10, sticky='ew')

Label(tab1, text="Category").grid(column=0, row=1, sticky='W')
categoryEntry = ttk.Combobox(tab1, values = choices)
categoryEntry.grid(column=1, row=1, pady=10, sticky='ew')

ttk.Button(tab1, text="Save", command=saveText).grid(column=0, row=2, sticky='ew')
ttk.Button(tab1, text="Export", command=exportToCsv).grid(column=1, row=2, pady=10, sticky='ew')

textListbox = Listbox(tab1)
textListbox.grid(column=0, row=3, columnspan=2, sticky='ew')

#TAB 2

Label(tab2, text="Capture Range").grid(column=0, row=0)

screenSizeConfig = Scale(tab2, from_=100, to=600, orient=HORIZONTAL)
screenSizeConfig.grid(row=1, columnspan=2, sticky='ew')

root.bind('<KeyPress>', getKeyDown)
root.mainloop()


# In[ ]:




