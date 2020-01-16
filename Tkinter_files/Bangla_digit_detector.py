from tkinter import *
from tkinter import ttk, colorchooser
from PIL import ImageGrab
import tkinter as tk
import win32gui
import pandas as pd
import numpy as np 
import itertools
import keras
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img 
from keras.models import Sequential 
from keras import optimizers
from keras.preprocessing import image
from keras.layers import Dropout, Flatten, Dense  
from keras import applications  
from keras.utils.np_utils import to_categorical  
import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
# %matplotlib inline
import math  
import datetime
import time
import joblib

class main:
    def __init__(self,master):
        self.master = master
        self.old_x = None
        self.old_y = None
        self.penwidth = 5
        self.drawWidgets()
        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)
        self.HWND = None
        main.text = None
        
    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,width=self.penwidth,capstyle=ROUND,smooth=True)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None      

    def changeW(self,e): #change Width of pen through slider
        self.penwidth = e
           

    def clear(drawWidgets):
        drawWidgets.c.delete(ALL)
        Label(drawWidgets.controls, text='Digit detected: --',font=('arial 18'),bg='green').grid(row = 2,column = 0)
    
    def detect_func(drawWidgets):
        rect = win32gui.GetWindowRect(main.HWND)
        # print(drawWidgets.x)
        ImageGrab.grab(bbox =rect).save('temp' + '.jpg')
        #####################
        def read_image(file_path):
    #     print("[INFO] loading and preprocessing image...")  
            image = load_img(file_path, target_size=(224, 224))  
            image = img_to_array(image)  
            image = np.expand_dims(image, axis=0)
            image /= 255.  
            return image
    
        
        def test_multiple_image(path):
            animals = ['0', '1','2','3','4','5','6','7','8','9']
            images = read_image(path)
            time.sleep(.5)
            bt_prediction = vgg16.predict(images)  
            preds = model.predict_proba(bt_prediction)
            class_predicted = model.predict_classes(bt_prediction)
            # print("ID: {}".format(class_predicted[0]))#, inv_map[class_predicted[0]]))  
            text = 'Digit detected: ' + str(class_predicted[0])
            Label(drawWidgets.controls, text=text,font=('arial 18'),bg='green').grid(row = 2,column = 0)
            return None
        
        
        path = 'temp.jpg'      
        test_multiple_image(path)
        # text = 'Digit detected: 9'
        # Label(drawWidgets.controls, text=text,font=('arial 18'),bg='green').grid(row = 2,column = 0)
        
        
    def drawWidgets(self):
        self.controls = Frame(self.master,padx = 2,pady = 2,width=400,height=30,bg='green')
        Label(self.controls, text='Pen Width:',font=('arial 10'),bg='green').grid(row=0,column=0)
        self.slider = ttk.Scale(self.controls,from_= 2, to = 20,command=self.changeW,orient=HORIZONTAL)
        self.slider.set(self.penwidth)
        self.slider.grid(row=0,column=1,ipadx=30)
        self.controls.pack(fill=BOTH,expand = 1)
            
        #button
        self.detect = Button(self.controls,text='Detect',width=30,height=2, command = self.detect_func)
        self.detect.grid(row = 1,column = 0)
        # self.b1.pack()
        
        Label(self.controls, text='Digit detected: --',font=('arial 18'),bg='green').grid(row = 2,column = 0)
        
        self.clear = Button(self.controls,text = "Clear",width=30,height=2,command=self.clear)
        self.clear.grid(row = 1,column = 1)
        # self.b2.pack()
        
        self.c = Canvas(self.master,width=400,height=300,bg='white')
        self.c.pack(fill=BOTH,expand=True)
        main.HWND = self.c.winfo_id()
        self.x = 10
        

if __name__ == '__main__':
    root = Tk()
    main(root)
    root.title('Bangla Digit Detector')
    vgg16 = joblib.load('mlbrain_CNNvgg.joblib')
    model = joblib.load('mlbrain_CNNmodel.joblib')
    # root.geometry("500x350+0+0")
    root.mainloop()