"""
Trojan Check Automation Bot
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import action_chains
from selenium.common.exceptions import NoSuchElementException

from twilio.rest import Client
import base64
import requests

from time import sleep
from Student import Student
import json

driver = webdriver.Safari() # Opens Safari


# Returns list of Student objects parsed from JSON 
def extractUserData(filename="users.json"):
    users = []
    data = []
    with open(filename, 'r') as f: 
        data = json.load(f)
    for line in data:
        newStudent = Student(line["username"], line["password"], line["phone_number"])
        users.append(newStudent)
    return users


# Waits until the Submit button loads then clicks it to proceed to next page
def clickSubmitButton(buttonName):
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, buttonName)))
    element.click()


# Checks off "No" for all buttons on a page
def clickNoButton(lowerNum, higherNum):
    i = lowerNum
    while i <= higherNum:
        elementID = 'mat-button-toggle-' + str(i) + '-button'
        driver.find_element(By.ID, elementID).click()
        i += 2


# Automation Bot that 
def automationBot(users):
    btnNames = ['.btn-login', '.submit-button.btn-next', '.btn-begin-assessment', '.btn-assessment-start', '.btn-next', '.btn-submit']

    for user in users:
        driver.get("https://trojancheck.usc.edu/login")

        clickSubmitButton(btnNames[0]) # Clicks login button

        # Inputs username and password to log in
        sleep(3)
        usernameInput = driver.find_element(By.ID, 'username')
        usernameInput.send_keys(user.username)
        passwordInput = driver.find_element(By.ID, 'password')
        passwordInput.send_keys(user.password)
        passwordInput.submit()
        sleep(10)   # Wait for user to do 2-factor authentication

        # Clicks various submit buttons to proceed
        for i in range(1,4):
            clickSubmitButton(btnNames[i])
            sleep(1)

        # "Are you up to date with your COVID vaccinations?" - not everyone gets asked this question
        driver.find_element(By.ID, "mat-button-toggle-1-button").click()
        clickSubmitButton(btnNames[4])

        # "Are you required to isolate?"
        clickNoButton(5, 5)     # Is (2, 2) for those who didn't get asked the COVID vaccine question
        clickSubmitButton(btnNames[4])

        # Checks off "No" for all COVID symptom responses
        clickNoButton(14, 26)   # Is (11, 23) for those who didn't get asked the COVID vaccine question
        clickSubmitButton(btnNames[4])
        sleep(1)

        # Checks off confirmation checkbox and submits
        driver.execute_script("arguments[0].click();", driver.find_element(By.ID, 'mat-checkbox-1-input'))
        clickSubmitButton(btnNames[5])

        # Screenshots the Trojan Check QR code
        driver.maximize_window()
        sleep(1)
        driver.execute_script("window.scrollTo(0, 250)") 
        driver.find_element(By.CSS_SELECTOR, '.day-pass-wrapper').screenshot('TrojanCheck.png')

        sleep(3)

        # Convert TC screenshot to base64 and upload to website
        with open("TrojanCheck.png", "rb") as file:
            url = "https://api.imgbb.com/1/upload"
            payload = {
                "key": "cf8939a790d1e4221645c27d1137f997",  # Personal key
                "image": base64.b64encode(file.read()),
            }
            res = requests.post(url, payload)
            objj = res.json()

        image_link = objj["data"]["url"]    # Image link to screenshot

        # Text image to student's phone number with Twilio SMS API
        account_sid = 'TWILIO SID'
        auth_token = 'TWILIO TOKEN'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                from_ = 'TWILIO NUMBER',
                media_url = [image_link],
                to = user.phone
            )
    
        driver.close()


def main():
    users = extractUserData()
    automationBot(users)


if __name__ == "__main__":
    main()
    driver.quit()
