import os
from dotenv import load_dotenv
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


load_dotenv()
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
EMAIL = os.getenv('EMAIL')

chrome_options = Options()
# chrome_options.add_argument("user-data-dir=/Users/lindsayqin/Library/Application Support/Google/Chrome")
# chrome_options.add_argument("profile-directory=Profile 1")


# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options) 
driver.get("https://be.my.ucla.edu/")
time.sleep(0.5) # Let the user actually see something!

myucla = driver.current_window_handle

username = driver.find_element("id", "logon")
username.send_keys(USERNAME)

password = driver.find_element("id", "pass")
password.send_keys(PASSWORD)

driver.find_element("xpath", "//*[@id='sso']/form/div/table/tbody/tr/td[1]/button").click()

time.sleep(3)
subprocess.run(["osascript", "-e", '''
            tell application "System Events"
                key down 53  # Press Escape
                delay 0.2
                key up 53    # Release Escape
            end tell
        '''])
time.sleep(1)
subprocess.run(["osascript", "-e", '''
            tell application "System Events"
                key down 53  # Press Escape
                delay 0.2
                key up 53    # Release Escape
            end tell
        '''])

try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div/div/div[1]/div[3]/div/button"))).click()
except:
    print("Couldn't find Other Options")

try:
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,  "/html/body/div/div/div[1]/div/div[1]/ul/li[5]/a"))).click()
except:
    print("Couldn't find phone 2")
    
driver.switch_to.new_window('window')
# driver.get("https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2fquestions")
# driver.find_element("xpath", "//*[@id='openid-buttons']/button[1]").click()
# email = driver.find_element("xpath", "//*[@id='identifierId']")
# email.send_keys(EMAIL)
# driver.find_element("xpath", "//*[@id='identifierNext']/div/button").click()




driver.get("https://voice.google.com/u/0/messages")

driver.find_element("xpath", "//*[@id='header']/div[2]/a[2]").click()

# email = driver.find_element("xpath", "//*[@id='identifierId']")
# email.send_keys(EMAIL)

# driver.find_element("xpath", "//*[@id='identifierNext']/div/button").click()


time.sleep(30)
driver.quit()
