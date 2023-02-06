#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pyautogui
import easyocr
import numpy as np
import csv
import os.path

from tkinter import *
from tkinter import ttk
from tkinter import filedialog


# In[64]:


def getText():
    focusBase = 100
    
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


# In[65]:


root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

choices = ['Tag', 'Valve', 'Line']

Label(frm, text="Text Value").grid(column=0, row=0)
textEntry = ttk.Entry(frm)
textEntry.grid(column=1, row=0,pady=10)

Label(frm, text="Category").grid(column=0, row=1)
categoryEntry = ttk.Combobox(frm, values = choices)
categoryEntry.grid(column=1, row=1, pady=10)

ttk.Button(frm, text="Save", command=saveText).grid(column=0, row=2)
ttk.Button(frm, text="Export", command=exportToCsv).grid(column=1, row=2, pady=10)

textListbox = Listbox(frm)
textListbox.grid(column=0, row=3, columnspan=2)

root.bind('<KeyPress>', getKeyDown)
root.mainloop()


# In[ ]:




