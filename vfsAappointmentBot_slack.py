from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import requests

def main():
	gmailId = "xxxx"
	passWord = "xxxx"
	no_data = "No appointment slots are currently available"
	hook_url = "xxxx"
	payload = {"text": "Not Available"}
	payload1 = {"text": "Dude, go for it"}
	try:
		driver = webdriver.Chrome(ChromeDriverManager().install())
		driver.get(r'https://visa.vfsglobal.com/ind/en/deu/login')
		driver.implicitly_wait(15)
		time.sleep(5)
		try:
			loginBox = driver.find_element_by_xpath('//*[@id ="mat-input-0"]')
			loginBox.send_keys(gmailId)
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			acceptAll = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div/div[1]/div/div[2]/div/button[3]")
			acceptAll.click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			passWordBox = driver.find_elements_by_xpath('/html/body/app-root/div/app-login/section/div/div/mat-card/form/div[2]/mat-form-field/div/div[1]/div[3]/input')
			passWordBox[0].send_keys(passWord)
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton = driver.find_elements_by_xpath('/html/body/app-root/div/app-login/section/div/div/mat-card/form/button')
			nextButton[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton1 = driver.find_elements_by_xpath('/html/body/app-root/div/app-dashboard/section/div/div[1]/div[2]/button')
			nextButton1[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton2 = driver.find_elements_by_xpath('/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[1]/mat-form-field')
			nextButton2[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton3 = driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/div/div/mat-option[11]/span')
			nextButton3[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton4 = driver.find_elements_by_xpath('/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[2]/mat-form-field')
			nextButton4[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton5 = driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/div/div/mat-option[2]/span')
			nextButton5[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton6 = driver.find_elements_by_xpath('/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[3]/mat-form-field')
			nextButton6[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			nextButton7 = driver.find_elements_by_xpath('/html/body/div[5]/div[2]/div/div/div/mat-option/span')
			nextButton7[0].click()
		except Exception as e:
			print(e)
		time.sleep(3)
		try:
			main = driver.find_elements_by_xpath('/html/body/app-root/div/app-eligibility-criteria/section/form/mat-card[1]/form/div[4]/div')
			data = main[0].get_attribute("innerHTML")
			print(time.strftime("%H:%M:%S", time.localtime()))
			print(data)
			if data.strip() == no_data:
				print("yes")
				resp = requests.post(hook_url,json=payload)
				if resp.status_code != 200:
					print("HTTP %s: %s" % (resp.status_code, resp.text))
			else:
				resp = requests.post(hook_url,json=payload1)
				if resp.status_code != 200:
					print("HTTP %s: %s" % (resp.status_code, resp.text))
				print("go for this dude")
		except Exception as e:
			print(e)
		driver.close()
	except Exception as e:
		print(e)
		print('Login Failed')

if _name_ == "_main_":
	while True:
		n = random.randint(15,20)
		time.sleep(n*60)
		main()
