from selenium import webdriver
import urllib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from twilio.rest import Client
#from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime


## VFS login email
email_str = 'your mail id'

## VFS password
pwd_str = 'your pass'
os.chdir(os.getcwd())

'''
I used the Twilio python API to be able to text myself with appointment alerts!
Twilio id, auth token, and twilio assigned phone number from Twilio free profile
For help, check out https://www.twilio.com/docs/libraries/python.
'''
account_sid = 'xxxxxxxxxxxxxxxxxxxx'
auth_token = 'xxxxxxxxxxxxxxxx'
twilio_client = Client(account_sid, auth_token)
twilio_phone = '+xxxxxxxxxxx'
## Replace this here with the phone number you'd like to recieve SMS at
my_phone = '+xxxxxxxxxxxxxxxxxxxxxxxxxxx'
browser = webdriver.Chrome(executable_path='chromedriver.exe')
log = open('vfslog.txt', 'w+')

'''
2Capcha is used to outsource solving the capchas - pay 50 cents / 1000 capchas solved.
Load 50 cents for an account and insert your api key below.
For help, check out https://github.com/athre0z/twocaptcha-api.

two_capcha_key = 'TWO CAPCHA API KEY'

no_appts = 'there are no appointments available at your chosen Visa Application Centre'
'''

def log_msg(log, message):
	now = datetime.now()
	date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
	log.write(date_time + "  ::  " + message + "\n")

def login(browser, log):
	## Login Page
	browser.get(('https://visa.vfsglobal.com/ind/en/deu/login'))
	time.sleep(4)
	print("Timeup")
	actions = ActionChains(browser)
	browser.find_element_by_id('onetrust-reject-all-handler').click()
	time.sleep(1)
	browser.find_element_by_id('mat-input-0').send_keys(email_str)
	#browser.find_element_by_name('Email').send_keys(email_str)
	browser.find_element_by_id('mat-input-1').send_keys(pwd_str)
	#Sign In Button hit
	browser.find_element_by_xpath('//button[@mat-raised-button]').click()
	time.sleep(10)
	print("\n--------------\nAPpoint ment Wait Over \n--------------\n")
	WebDriverWait(browser,100).until(EC.presence_of_element_located((By.XPATH, '//*[contains(string(.), " Start New Booking ")]')))
	print("\n--------------\nWait Over \n--------------\n")
	#Start New Appointment Button hit
	browser.find_element_by_xpath("//button[@class='mat-focus-indicator btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base']").click()
	#browser.find_element_by_xpath('//button[@mat-raised-button]').click()
	# btn mat-btn-lg btn-block btn-brand-orange mat-raised-button mat-button-base"]')
	#elem.click()
	time.sleep(4)
	print("Appointment but hit done ----------------------")
	#Select Mumbai Button hit
	browser.find_element_by_xpath('//mat-option[@class="mat-option mat-focus-indicator ng-tns-c84-26 ng-star-inserted"][9]').click()
	time.sleep(2)
	print("Mumbai but hit done ----------------------")
	#long term Button hit
	browser.find_element_by_xpath("//mat-option[@class='mat-option mat-focus-indicator ng-tns-c84-28 ng-star-inserted'][2]").click()
	time.sleep(2)
	print("Longteem but hit done ----------------------")
	#Blue card Button hit
	browser.find_element_by_xpath("//mat-option[@class='mat-option mat-focus-indicator ng-tns-c84-30 ng-star-inserted'][1]").click()
	time.sleep(2)
	print("Final but hit done ----------------------")
	#Scroll one down
	#win32api.mouse_event(MOUSEEVENTF_WHEEL, x, y, -1, 0)


def alert_for_appointment(browser,log):
	## Returns a tuple, (Session expired, AppointmentAvailable)
	time.sleep(3)
	## Switches over to the new tab with appointment availability.
	browser.switch_to_window(browser.window_handles[1])
	#browser.save_screenshot("appointmentImage.png")
	if (no_appts not in browser.page_source):
		if check_session_expired(browser, log):
			browser.close()
			browser.switch_to_window(browser.window_handles[0])
			return (True, False)
		log_msg(log, "FOUND APPOINTMENTS!")
		browser.save_screenshot("appointmentImage.png")

		message = twilio_client.messages\
			.create(
				body = 'THERE ARE APPOINTMENTS!! AHH!!',
				from_= twilio_phone, 
				to= my_phone)
		return (check_session_expired(browser, log), True)
	else:
		log_msg(log, "No appointments available.")
	browser.close()
	browser.switch_to_window(browser.window_handles[0])
	return (check_session_expired(browser, log), False)

def check_appointment(browser, log):
	## Returns a tuple, (Session expired, AppointmentAvailable)
	time.sleep(2)
	if check_session_expired(browser, log):
		return (True, False)
	browser.find_element_by_name('Start New Booking').click()
    #browser.find_element_by_id('Documentupload').click()
	#continue_btn = browser.find_element_by_id('btn_continue')
	'''
	This is the action keys to right click on the continue button
	(to open the resulting page in a new tab).  You'd need to change
	this action sequence if you're not on a Mac.
	'''
	ActionChains(browser) \
	   	.key_down(Keys.COMMAND) \
	   	.click(continue_btn) \
	   	.key_up(Keys.COMMAND) \
	   	.perform()
	return alert_for_appointment(browser, log)

def check_session_expired(browser, log):
	if 'Session timeout' in browser.page_source:
		log_msg(log, "Session expired.")
		return True
	return False

def monitor_appointments():
	## Potentially change this path for wherever you have installed the chromedriver.
	#browser = webdriver.Chrome(executable_path='chromedriver.exe')
	#solver = TwoCaptcha(two_capcha_key)
	actions = ActionChains(browser)
	#log = open('vfslog.txt', 'w+')
	appointments = False
	#login(browser, log)
	time.sleep(7)
	print("Start new app click by linktexxt -------------")
	print("Login successful-------------")
	while True:
		login(browser, log)
		#print("Login successful-------------")
		"""while not appointments:
			(expired, appointments) = check_appointment(browser, log)
			if expired:
				break
		if appointments:
			return"""

login(browser, log)

#monitor_appointments()
