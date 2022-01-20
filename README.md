# TrojanCheckAutomation
App that automates the daily Trojan Check process at USC (logs in, fills in responses, etc.) and sends a screenshot of the QR code to the student's phone number. 

## Details
This bot uses Selenium to interact with the USC Trojan Check website and Twilio SMS API to send the screenshot of the QR code through text message. It is also 
implemented & scheduled on PythonAnywhere (does not come with code) so that the automation runs every day at midnight. 

## How to use
1. Install Selenium and Twilio
```bash
pip install selenium
pip install twilio
```
2. Fill in the student information in the users.json file. **Phone number must include country code (+1 for US)**

3. Run the program with Python 
```bash
python TCBot.py
```

## Contributors
Credits to Jevon Torres, my fellow CS classmate, who inspired this project and wrote the portion of the code that uploads the screenshot & texts it to the student.
He also figured out how to use the Twilio API and scheduled the bot on PythonAnywhere. 
