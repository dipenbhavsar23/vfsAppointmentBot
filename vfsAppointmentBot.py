import pyautogui
import time
import pyscreenshot as ImageGrab
from PIL import * 
import numpy as np
import cv2
from pixelmatch import pixelmatch
from twilio.rest import Client
from datetime import datetime
import random
from playsound import playsound
import os 
'''
Twilio python API to be able to text myself with appointment alerts!
Twilio id, auth token, and twilio assigned phone number from Twilio free profile
For help, check out https://www.twilio.com/docs/libraries/python.
'''
account_sid = 'XXXXXXXXXXXXXXXXX' #Sid from Twillo
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXX' #generated token from Twillo
twilio_client = Client(account_sid, auth_token)
twilio_phone = 'XXXXXXXXXXX'  #your Twillo phone number
## Replace this here with the phone number you'd like to recieve SMS at
my_phone = '+91XXXXXXXXXXX' #your phone number [anycontry]
seq_num = 1
c_minThrs = 1
c_maxThrs = 2
toggleFlag = True
os.chdir(os.getcwd())
'''
    Function to compare image 
    Parameters:
    image -     Current screenshot
    template -  referece image (take reference by selecting section like certificate 
                where appointments are always available. change the name by countinuebutton.png)
    value -     Threshold of image comparision (keep less then 20%) you can finetune as per your req.
''' 
def match_img(image, template, value):

    res = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    threshold = value
    min_v, max_v, min_pt, max_pt = cv2.minMaxLoc(res)
    if max_v < threshold:
        return False
    if not max_pt[0] in range(10, 40) or max_pt[1] > 20:
        return False
    return max_pt 
    

while True:
#every seq wait for for webpage
    time.sleep(2)
    '''toggling the dropdown list ---> if and else serves the same purpose,
        VFS able to catch if you run same selection all time so better tried to make it more human like
        you can set threshold for time randomness
    '''
    if toggleFlag == True:
        pyautogui.press('up')
        time.sleep(random.randint(c_minThrs,c_maxThrs))
        pyautogui.press('down')
        time.sleep(random.randint(c_minThrs,c_maxThrs))
        toggleFlag = False
    elif toggleFlag == False:
        pyautogui.press('down')
        time.sleep(random.randint(c_minThrs,c_maxThrs))
        pyautogui.press('up')
        time.sleep(random.randint(c_minThrs,c_maxThrs))
        toggleFlag = True
    image = pyautogui.screenshot()
    time.sleep(random.randint(3,10))
    image = cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    image_arr = image[600:700, 150:1150]
    # writing it to the disk using opencv
    cv2.imwrite("/temp.png", image_arr)
    time.sleep(1)
    #reference image [Try to make for your self]
    i1 = Image.open('countinuebutton.png')
    #keep as is -- image SS by each seq
    i2 = Image.open('temp.png')
    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
    ncomponents = i1.size[0] * i1.size[1] * 3
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    seq_num=seq_num+1
    #prints logs with Seq number, time, difference 
    print ("Seq No: ", seq_num, "Current Time =", current_time,"Difference (percentage):", (dif / 255.0 * 100) / ncomponents)
    ''' Text msg trigger
        it will play song along with sending msg [Suggestion: keep your laptop/desktop volume to to max...]'''
    if ((dif / 255.0 * 100) / ncomponents) <= 10:
        message = twilio_client.messages\
		.create(
		body = 'Monster: Run Appointment is Available......',
		from_= twilio_phone, 
		to= my_phone)
        browser = webdriver.Chrome(executable_path='chromedriver.exe')
        #Darkside starts with high bits so appointment gets first attention ;)
        browser.get(('https://youtu.be/m-PJmmvyP10?t=45'))
        time.sleep(6)
        pyautogui.press('space')
        break
    print("____________ SEQ COMPLETE ____________")
