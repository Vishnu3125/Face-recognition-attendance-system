# Face-recognition-attendance-system

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)   

### Code Requirements (python libraries)
- Opencv(`pip install opencv-python`)
- Tkinter(Available in python)
- PIL (`pip install Pillow`)
- Pandas(`pip install pandas`)

### What steps you have to follow??
- Download this Repository 
- Create a `TrainingImage` folder in a project.
- Open `FRAMS.py` and change the all paths with your system path
- Run `FRAMS.py`.

### Project Structure

- After run you need to give your face data to system so enter your ID and name in box than click on `Take Images` button.
- It will collect 60 images of your faces, it save a images in `TrainingImage` folder
- After that we need to train a model(for train a model click on `Train Model` button.
- It will take 5-10 minutes for training(for 10 person data).
- After training click on `Automatic Attendance` ,it can fill attendace by your face using our trained model (model will save in `TrainingImageLabel` )
- it will create `.csv` file of attendance according to time & subject.
- You can store data in database (install wampserver),change the DB name according to your in `FRAMS.py`.
- `Manually Fill Attendace` Button in UI is for fill a manually attendance (without facce recognition),it's also create a `.csv` and store in a database.

### Screenshots

#### Main page
![img](Src/1.png)

#### Admin UI
![img](Src/2.png)

![img](Src/3.png)

![img](Src/4.png)

#### Student UI
![img](Src/6.png)

![img](Src/7.png)

### Notes
- It will require high processing power(I have 8 GB RAM & 2 GB GC)
- accuracy of this project recoginition is moderate
- Noisy image can reduce your accuracy so quality of images matter.
