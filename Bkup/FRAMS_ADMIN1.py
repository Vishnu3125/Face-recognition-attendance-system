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


####GUI for manually fill attendance
def manually_fill():
    global sb
    sb = tk.Tk()
    sb.title("Work Under Process")
    sb.geometry('480x286')
    sb.configure(background='snow')
    Lab1 = Label(sb, text= "This is additional feature, this feature will be available in next update")
    Lab2 = Label(sb, text= " - Thank you !!!")
    Lab1.place(x=10, y= 30)
    Lab2.place(x=10, y=50)

##For clear textbox
def clear():
    txt.delete(first=0, last=22)
def clear1():
    txt2.delete(first=0, last=22)
    
##Error screen1
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='#4D4D4D')
    Label(sc1,text='Enrollment & Name required!!!',fg='snow',bg='#4D4D4D',font=('times', 16, ' bold ')).pack()
    photo = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/quit1.png")
#    Button(sc1, text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=30  ,height=30, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)
    button2 = Button(sc1, text='OK',command=del_sc1, width=4  ,height=1)
    button2.place(x=120, y= 50)

##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.iconbitmap('FRAMS.ico')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

###For take images for datasets
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
            #cam.set(cv2.CAP_PROP_FRAME_WIDTH, 450)
            #cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)
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
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 70
                elif sampleNum > 150:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            clear()
            clear1()
            res = "Images Saved for Enrollment : " + Enrollment + " and Name : " + Name
            Notification.configure(text=res, bg="#a4c46c", width=65, font=('times', 8, 'bold'))
            Notification.place(x=80, y=215)
        except FileExistsError as F:
            f = 'Student Data already exists'
            Notification.configure(text=f, bg="Red", width=21)
            Notification.place(x=60, y=215)


###for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        global Subject
        Subject = tx.get()
        sub=tx.get()
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                try:
                    recognizer.read("TrainingImageLabel/Trainner.yml")
                except:
                    e = 'Model not found,Please train model'
                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 10, 'bold'))
                    Notifica.place(x=20, y=210)
                    return

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
                        if (conf <70):
                            print(conf)
                            # global Subject
                            global aa
                            global date
                            global timeStamp
                            print (tx.get())
                            # Subject = "DIP"#tx.get()
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
                Notifica.configure(text=M, bg="Green", fg="white", width=33, font=('times', 10, 'bold'))
                Notifica.place(x=20, y=180)

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
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 12, ' bold '), bg="lawn green", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
                print(attendance)

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.title("select subject name...")
    windo.geometry('480x286')
    windo.configure(background='snow')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="Green", fg="white", width=33, height=2, font=('times', 15, 'bold'))

    def Attf():
        import subprocess
        subprocess.Popen(r'explorer /select,"/home/pi/Desktop/frams/Attendance/Manually\ Attendance/"')  #open attendance sheet window

    attf = tk.Button(windo,  text="Check",command=Attf,fg="black"  ,bg="lawn green"  ,width=8  ,height=1 ,activebackground = "Red" ,font=('times', 10, ' bold '))
    attf.place(x=400, y=255)

    sub = tk.Label(windo, text="Select Subject", width=15, height=2, fg="white", bg="blue2", font=('times', 12, ' bold '))
    sub.place(x=50, y=70)
    
    tx = StringVar(windo)
    tx.set("PYTHON-PRAC")

    opt = OptionMenu(windo, tx, "AI", "SC", "DIP", "IS", "PYTHON", "PYTHON-PRAC")
    opt.place(x =200, y = 70)

# This is the option to add entry box insted of optionmenu
#    tx = tk.Entry(windo, width=20, bg="yellow", fg="red", font=('times', 20, ' bold '))
#    tx.place(x=200, y=70)

    fill_a = tk.Button(windo, text="Fill Attendance", fg="white",command=Fillattendances, bg="light green", width=20, height=2, activebackground="Red", font=('times', 10, ' bold '))
    fill_a.place(x=100, y=130)
    windo.mainloop()

def admin_panel():
    import csv
    import tkinter
    root = tkinter.Tk()
    root.title("Student Details")
    root.configure(background='snow')

    cs = '/home/pi/Desktop/frams/StudentDetails/StudentDetails.csv'
    with open(cs, newline="") as file:
        reader = csv.reader(file)
        r = 0

        for col in reader:
            c = 0
            for row in col:
                label = tkinter.Label(root, width=12, height=1, fg="black", font=('times', 10, ' bold '), bg="#f0ffdb", text=row, relief=tkinter.RIDGE)
                label.grid(row=r, column=c)
                c += 1
            r += 1
    root.mainloop()


###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")

    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=60, y=210)
        return
    try:
        recognizer.train(faces, np.array(Id))
    except:
        Notification.configure(text="No student information found !!!", bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=60, y=210)
        return

    try:
        recognizer.write("TrainingImageLabel/Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="#a4c46c", width=50, font=('times', 10, 'bold'))
        Notification.place(x=60, y=240)
        return

    res = "Model Trained"
    Notification.configure(text=res, bg="#a4c46c", width=50, font=('times', 10, 'bold'))
    Notification.place(x=60, y=215)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

def stats():
    filename=os.listdir('Attendance')
    df=pd.read_csv("StudentDetails\StudentDetails.csv")

    print(df)

    print(filename)


if __name__ == '__main__':
    #####Window is our Main frame of system
    
    # #B1D877=green, #F16A70=red, #8CDCDA=blue, #4D4D4D=black
    # #a4c46c=dark green, #e66165=dark red
    
    colour_lab_bg = "#B1D877"
    colour_lab_txt = "#4D4D4D"
    
    colour_entry_bg = "#4D4D4D"
    colour_entry_txt = "white"
    
    colour_clear_bg = "#B1D877"
    colour_clear_abg = "#B1D877"
    colour_clear_txt = "black"
    
    colour_button_bg = "#B1D877"
    colour_button_abg = "#a4c46c"
    colour_button_txt = "black"
    
    colour_main = "#B1D877"
    
    
    window = tk.Tk()
    window.title("Face Recognition Based Attendance System")

    window.geometry('480x286') #480x286 1280x720
    window.configure(background=colour_main)

    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)
 #   window.iconbitmap('FRAMS.ico')

    def on_closing():
        from tkinter import messagebox
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            window.destroy()
    window.protocol("WM_DELETE_WINDOW", on_closing)

    message = tk.Label(window, text="Face-Recognition-Based-Attendance-System", bg=colour_main, fg="#4D4D4D", width=40,
                       height=2, font=('times', 16, 'italic bold '))

    message.place(x=10, y=0)

    Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                          height=2, font=('times', 12, 'bold'))

    lbl = tk.Label(window, text="Enter Enrollment", width=16, height=1, fg=colour_lab_txt, bg=colour_lab_bg, anchor=E, font=('times', 11, ' bold '))
    lbl.place(x=75, y=60)

    def testVal(inStr,acttyp):
        if acttyp == '1': #insert
            if not inStr.isdigit():
                return False
        return True

    txt = tk.Entry(window, validate="key", width=24, bg=colour_entry_bg, bd=0, fg=colour_entry_txt, highlightthickness = 0,font=('times', 8, ' bold '))
    txt['validatecommand'] = (txt.register(testVal),'%P','%d')
    txt.place(x=200, y=65)

    lbl2 = tk.Label(window, text="Enter Name", width=16, fg=colour_lab_txt, bg=colour_lab_bg, height=1, anchor=E, font=('times', 11, ' bold '))
    lbl2.place(x=75, y=90)

    txt2 = tk.Entry(window, width=24, bg=colour_entry_bg, bd=0, fg=colour_entry_txt, highlightthickness = 0, font=('times', 8, ' bold '))
    txt2.place(x=200, y=95)

    photo = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/quit1.png")
    clearButton = tk.Button(window, image=photo,text="Clear",command=clear,fg=colour_clear_txt  ,bg=colour_clear_bg  , highlightthickness = 0, bd=0 , width=15  ,height=15 ,activebackground = colour_clear_abg ,font=('times', 8, ' bold '))
    clearButton.place(x=330, y=65)

    clearButton1 = tk.Button(window, image=photo,text="Clear",command=clear1,fg=colour_clear_txt  ,bg=colour_clear_bg  , highlightthickness = 0,bd=0, width=15 ,height=15, activebackground = colour_clear_abg ,font=('times', 8, ' bold '))
    clearButton1.place(x=330, y=95)

    photo1 = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/photo1.png")
    takeImg = tk.Button(window, image = photo1, compound = TOP,text="Take Images" ,command=take_img,fg=colour_button_txt  ,bg=colour_button_bg, bd=0, highlightthickness = 0, width=80  ,height=80, activebackground = colour_button_abg,font=('times', 9))
    takeImg.place(x=30, y=125)

    photo2 = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/process.png")
    trainImg = tk.Button(window, image = photo2, compound = TOP,text="Train Model",fg=colour_button_txt,command=trainimg ,bg=colour_button_bg, bd=0, highlightthickness = 0, width=80  ,height=80, activebackground = colour_button_abg ,font=('times', 9))
    trainImg.place(x=134, y=125)

    photo3 = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/check.png")
    FA = tk.Button(window, image = photo3, compound = TOP, text="Attendance",fg=colour_button_txt,command=subjectchoose  ,bg=colour_button_bg, bd=0, highlightthickness = 0, width=80  ,height=80, activebackground = colour_button_abg ,font=('times', 9))
    FA.place(x=238, y=125)
    
    photo4 = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/list.png")
    AP = tk.Button(window, image = photo4, compound = TOP, text="Registered students", command=admin_panel, fg=colour_button_txt  ,bg=colour_button_bg, bd=0, highlightthickness = 0, width=80 ,height=80, activebackground = colour_button_abg ,font=('times', 9))
    AP.place(x=342, y=125)

#    photo4 = PhotoImage(file = r"/home/pi/Desktop/frams/Icon/question.png")
#    quitWindow = tk.Button(window, image = photo4,text="Manually Fill Attendance", command=manually_fill  ,fg=colour_button_txt, bd=0 , highlightthickness = 0,bg=colour_button_bg  ,width=40  ,height=30, activebackground = colour_button_abg ,font=('times', 9, ' bold '))
#    quitWindow.place(x=250, y=180)

#    Stats = tk.Button(window, text="Statistics", fg="white", command=stats, bg="grey", borderwidth=2, width=9, height=1, activebackground="Red", font=('times', 10, ' bold '))
#    Stats.place(x=350, y=140)

    window.mainloop()