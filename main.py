import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Telegram Support URL
REPORT_URL = "https://telegram.org/support"

# List of Emails for Reporting (Change these)
email_accounts = [
    "imvoid1001@gmail.com",
    "imvoid1002@gmail.com",
    "imvoid1003@gmail.com",
    "imvoid1004@gmail.com"
    "imvoid1005@gmail.com"
    "imvoid1006@gmail.com"
    "imvoid1007@gmail.com"
    "imvoid1008@gmail.com"
    "imvoid1009@gmail.com"
    "imvoid1010@gmail.com"
    "scorching02@gmail.com"
    "scorching01@gmail.com"
]
import pyfiglet
from termcolor import colored

def print_heading(text, color="cyan"):
    ascii_art = pyfiglet.figlet_format(text)
    colored_text = colored(ascii_art, color)
    print(colored_text)

# Example usage
print_heading("The Massacres", "red")


# Load Proxies from proxies.txt
def load_proxies():
    """ Reads proxies from proxies.txt """
    with open("proxies.txt", "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

# Load proxies
proxies = load_proxies()
if not proxies:
    print("❌ No proxies found in proxies.txt! Add some and try again.")
    exit()

# User Inputs
channel_name = input("Enter the channel name to report: ")
channel_link = input("Enter the Telegram channel link: ")
reason_text = input("Enter the reason for reporting: ")
num_reports = int(input("How many reports to send? "))

def report_channel(email, proxy):
    """ Submits a report using a given email and SOCKS5 proxy """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Set SOCKS5 Proxy
    chrome_options.add_argument(f"--proxy-server=socks5://{proxy}")

    # Start WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
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
        print(f"✅ Report sent via {email} using proxy {proxy}")
        
        # Log report submission
        with open("reports_log.txt", "a") as log_file:
            log_file.write(f"Report Sent via {email} using {proxy} at {time.ctime()}\n")

    except Exception as e:
        print(f"❌ Failed to send report via {email} using {proxy}: {e}")

    finally:
        driver.quit()

# Run reports with email & proxy rotation
for _ in range(num_reports):
    email = random.choice(email_accounts)  # Select a random email
    proxy = random.choice(proxies)  # Select a random proxy
    report_channel(email, proxy)
    time.sleep(60)  # Wait before next submission
