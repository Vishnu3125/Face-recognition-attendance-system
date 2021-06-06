import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time


##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
#   sc2.iconbitmap('FRAMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

def Fillattendances():
    sub = tx.get()
    now = time.time()  ###For calculate seconds of video
    future = now + 20
    if time.time() < future:
        if sub == '':
            err_screen1()
        else:
            recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
            try:
                recognizer.read("TrainingImageLabel/Trainner.yml")
            except:
                e = 'Model not found,Please train model'
                Notifica.configure(text=e, bg="4d4d4d", fg="white", width=33, font=('times', 15, 'bold'))
                Notifica.place(x=20, y=220)

            harcascadePath = "haarcascade_frontalface_default.xml"
            faceCascade = cv2.CascadeClassifier(harcascadePath)
            df = pd.read_csv("StudentDetails/StudentDetails.csv")
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ['Enrollment', 'Name', 'Date', 'Time']
            attendance = pd.DataFrame(columns=col_names)
            while True:
                ret, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    global Id

                    Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    if (conf < 70):
                        print(conf)
                        global Subject
                        global aa
                        global date
                        global timeStamp
                        Subject = tx.get()
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        aa = df.loc[df['Enrollment'] == Id]['Name'].values
                        global tt
                        tt = str(Id) + "-" + aa
                        En = '15624031' + str(Id)
                        attendance.loc[len(attendance)] = [Id, aa, date, timeStamp]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (255, 255, 0,), 4)

                    else:
                        Id = 'Unknown'
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                        cv2.putText(im, str(tt), (x + h, y), font, 1, (0, 25, 255), 4)
                if time.time() > future:
                    break

                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                cv2.imshow('Filling attedance..', im)
                key = cv2.waitKey(30) & 0xff
                if key == 27:
                    break

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance/" + Subject + "_" + date + "_" + Hour + "-" + Minute + "-" + Second + ".csv"
            attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
            print(attendance)
            attendance.to_csv(fileName, index=False)

            M = 'Attendance filled Successfully'
            Notifica.configure(text=M, bg="#61605f", fg="white", width=33, font=('times', 10, 'bold'))
            Notifica.place(x=115, y=180)
            cam.release()
            cv2.destroyAllWindows()

            import csv
            import tkinter
            root = tkinter.Tk()
            root.title("Attendance of " + Subject)
            root.configure(background='snow')
            cs = '/home/pi/Desktop/frams/' + fileName
            with open(cs, newline="") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 11, ' bold '), bg="#ffd9d9", text=row, relief=tkinter.RIDGE)
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1
            root.mainloop()
            print(attendance)


if __name__ == '__main__':

    windo = tk.Tk()
    windo.title("Student panel")
    windo.geometry('480x286')
    windo.configure(background='#F16A70')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33, height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
      #  subprocess.Popen(r'explorer /select,/home/pi/Desktop/frams/Attendance')  #open attendance sheet window
        subprocess.Popen(r'home\pi\Desktop\frams\Attendance')
        
    message = tk.Label(windo, text="Student Face ID Attandance", bg="#F16A70", fg="#4D4D4D", width=37, height=2, font=('times', 18, 'italic bold '))
    message.place(x=10, y=0)

    sub = tk.Label(windo, text="Select Subject", width=15, height=2, fg="#4D4D4D", bg="#F16A70", font=('times', 13, ' bold '))
    sub.place(x=58, y=68)

    tx = Combobox(windo, values = ["AI", "SC", "IS", "DIP", "PYTHON", "PYTHON-PRAC"], background = "black", foreground= "black", width = 20)
    tx.current(0)
    tx.place(x =200, y = 80)

#    This is the option to add entry box insted of optionmenu
#    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 20, ' bold '))
#    tx.place(x=200, y=70)

    fill_a = tk.Button(windo, text="Fill Attendance",command=Fillattendances, bg="#4D4D4D", fg="white", width=20, height=2, activebackground="#403f3f", activeforeground="white",bd = 0, highlightthickness = 0, font=('times', 10, ' bold '))
    fill_a.place(x=150, y=120)
    
    attf = tk.Button(windo,  text="Check",command=Attf,fg="white"  ,bg="#4D4D4D"  ,width=8  ,height=1 ,activebackground = "#403f3f", activeforeground="white", bd = 0, highlightthickness = 0, font=('times', 10, ' bold '))
    attf.place(x=395, y=255)

    windo.mainloop()