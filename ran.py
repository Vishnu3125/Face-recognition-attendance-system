import random
import string
import random
import pyautogui
import time
# printing lowercase
time.sleep(5)
for f in range(5000):
    letters = string.ascii_lowercase
    #print ( ''.join(random.choice(letters) for i in range(random.randint(3,5))))
    pyautogui.write(''.join(random.choice(letters) for i in range(random.randint(5,9))))
    pyautogui.press('enter')
    time.sleep(0.2)
