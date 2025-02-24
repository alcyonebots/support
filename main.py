import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pyfiglet
from termcolor import colored

# Telegram Support URL
REPORT_URL = "https://telegram.org/support"

# Fix Email List Formatting
email_accounts = [
    "imvoid1001@gmail.com", "imvoid1002@gmail.com", "imvoid1003@gmail.com",
    "imvoid1004@gmail.com", "imvoid1005@gmail.com", "imvoid1006@gmail.com",
    "imvoid1007@gmail.com", "imvoid1008@gmail.com", "imvoid1009@gmail.com",
    "imvoid1010@gmail.com", "scorching02@gmail.com", "scorching01@gmail.com"
]

# Print ASCII Header
def print_heading(text, color="cyan"):
    ascii_art = pyfiglet.figlet_format(text)
    colored_text = colored(ascii_art, color)
    print(colored_text)

print_heading("The Massacres", "red")

# Load Proxies from proxies.txt
def load_proxies():
    """ Reads proxies from proxies.txt """
    with open("proxies.txt", "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

proxies = load_proxies()
if not proxies:
    print("❌ No proxies found in proxies.txt! Add some and try again.")
    exit()

# User Inputs
channel_name = input("Enter the channel name to report: ")
channel_link = input("Enter the Telegram channel link: ")
reason_text = input("Enter the reason for reporting: ")
num_reports = int(input("How many reports to send? "))

# Initialize WebDriver Once
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

# Start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def report_channel(email, proxy, report_number):
    """ Submits a report using a given email and SOCKS5 proxy """
    chrome_options.add_argument(f"--proxy-server=socks5://{proxy}")  # Set proxy
    driver.get(REPORT_URL)
    time.sleep(2)  # Allow page to load

    try:
        # Fill out the form
        driver.find_element(By.NAME, "your_email").send_keys(email)
        driver.find_element(By.NAME, "description").send_keys(
            f"Channel Name: {channel_name}\nLink: {channel_link}\nReason: {reason_text}"
        )
        time.sleep(1)

        # Submit the report
        driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
        print(f"✅ Report #{report_number} sent via {email} using proxy {proxy}")
        
        # Log report submission
        with open("reports_log.txt", "a") as log_file:
            log_file.write(f"Report #{report_number} sent via {email} using {proxy} at {time.ctime()}\n")

    except Exception as e:
        print(f"❌ Failed to send report #{report_number} via {email} using {proxy}: {e}")

# Run reports with email & proxy rotation
for i in range(1, num_reports + 1):
    email = random.choice(email_accounts)
    proxy = random.choice(proxies)
    report_channel(email, proxy, i)
    time.sleep(60)  # Wait before next submission

# Close WebDriver
driver.quit()
