import os
from selenium import webdriver
from dotenv import load_dotenv

load_dotenv()

def setup_chrome_driver():
    chrome_options = webdriver.ChromeOptions()

    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1250x600")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    chrome_options.add_argument(f'user-agent={os.getenv("USER_AGENT")}')
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # chrome_options.add_argument(f'--user-data-dir={os.getenv("USER_DATA_DIR")}')
    # chrome_options.add_argument("user-data-dir=/Users/<Your-Username>/Library/Application Support/Google/Chrome/Default")

    # chrome_options.add_argument('--proxy-server=geo.iproyal.com:12321')
    # chrome_options.add_argument('--proxy-server=geo.iproyal.com:12321:mGe8NFtxAXpIGd71:8ficOKcwjCkE3TYG')

    return webdriver.Chrome(options=chrome_options)