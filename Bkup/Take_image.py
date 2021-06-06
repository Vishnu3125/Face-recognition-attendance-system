import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time


def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 70:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('\home\pi\Desktop\main\StudentDetails\StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for Enrollment : " + Enrollment + " Name : " + Name
            Notification.configure(text=res, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
            Notification.place(x=30, y=220)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=450, y=400)
            
            
tk = Tk()
tk.geometry("480x286")
#tk.configure(bg="Light Green")

lbl = Label(tk, text="Enter Enrollment", width=16, height=1, fg="black", bg="cyan", font=('times', 10, ' bold '))
lbl.place(x=60, y=45)

def testVal(inStr,acttyp):
        if acttyp == '1': #insert
            if not inStr.isdigit():
                return False
        return True

txt = Entry(tk, validate="key", width=24, bg="snow", fg="red", font=('times', 8, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=200, y=45)

lbl2 = Label(tk, text="Enter Name", width=16, fg="black", bg="cyan", height=1, font=('times', 10, ' bold '))
lbl2.place(x=60, y=75)

txt2 = Entry(tk, width=24, bg="snow", fg="red", font=('times', 8, ' bold '))
txt2.place(x=200, y=75)

button1 = Button(tk, text="Take Image", command=take_img, bg="cyan")
button1.place(x=140, y=120)

tk.mainloop()