import os
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

def setup_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1250x600")

    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'user-agent={os.getenv("USER_AGENT")}')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    return webdriver.Chrome(options=chrome_options)