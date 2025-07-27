**Telegram RAT with Social Engineering Login Page**

Description:
A Python-based Remote Access Tool (RAT) that uses a fake HTML login page as a social engineering entry point. Once the victim submits their credentials, the RAT is triggered, allowing remote control through a Telegram bot.

Disclaimer:
This tool is for educational and authorized security testing purposes only. Unauthorized use of this software against systems you do not own or have permission to test is illegal and strictly discouraged.

------------------------------------------------------------------
**Features:**

Telegram Bot C2 – Control the victim machine remotely via Telegram.

Social Engineering Attack – Fake lottery-winning HTML page tricks the user into logging in.

Credential Harvesting – Captured credentials are saved to creds.txt.

Screenshot Capture

Clipboard Data Extraction

File Upload, Download and Run

Process Listing

Shell Command Execution 

---------------------------------------
**Setup and Usage:**

Clone the Repository:
Clone this project using git and navigate into the directory.

Install Requirements:
Run pip install -r requirements.txt to install all required Python packages.

Configure Telegram Bot:
Create a bot via @BotFather on Telegram. Replace your bot token and authorized user ID in rat.py.

Host the Fake Login Page:
Use Python’s HTTP server or any web server to host the login.html file. For example:
Run this in the templates folder: python -m http.server 8080
Then share the link (http://your-ip:8080/login.html) with the victim.

Run the RAT:
Launch the server.py script. It will monitor creds.txt and trigger remote control functionality once credentials are received.

-------------------------------------------------------------------------------------
**Requirements:**

Python 3.8 or higher

Required modules: requests, pyautogui, telepot, psutil, pyperclip, etc.

Security Notes:

Communication between the client and the controller is done through Telegram, which is encrypted.

Captured credentials are stored in plaintext inside creds.txt. Secure this file appropriately.

Some features may require admin privileges or may work only on specific operating systems.

To-Do / Future Improvements:

Fix currently non-working features like shell execution and screen recording.

Add credential encryption.

Improve anti-detection techniques.

Add GUI for attacker-side control (optional).
