import os
import time
from dotenv import load_dotenv
from driver import setup_chrome_driver
from flask import Flask, request, jsonify
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'status': True,
        'message': 'Welcome to Privnote API',
        'statusCode': 200,
        'data': []
    }), 200


@app.route('/create-secret-note', methods=['POST'])
def create_secret_note():
    driver = setup_chrome_driver()
    actions = ActionChains(driver)

    try:
        secret_note = request.json.get("secret_note")
        privnote_url = os.getenv("PRIV_URL") 

        driver.get("https://privnote.com/")
        driver.execute_script("window.scrollBy(0, 1000);")

        textarea = WebDriverWait(driver, 10).until(
            # EC.presence_of_element_located((By.NAME, "note_text"))
            EC.presence_of_element_located((By.NAME, "note_raw"))
        )

        textarea.clear()
        textarea.send_keys(secret_note)
        time.sleep(5)

        # button = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.ID, "encrypt_note"))
        # )
        # button.click()

        button = driver.find_element(By.ID, "encrypt_note")
        actions.move_to_element(button).click().perform()
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(15)

        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "note_link_input"))
        )
        input_content = input_element.get_attribute("value")

        print('secret note link')
        print(input_content)

        time.sleep(5)

        current_url = driver.current_url
        print(f"The current URL is: {current_url}")

        # Find the element by its ID
        email_link_element = driver.find_element(By.ID, "mailto_link")
        href_value = email_link_element.get_attribute("href")
        print(f"The privnote URL is: {href_value}")
        
        return jsonify({
            'status': True,
            'message': 'Secret note link retrieved successfully',
            'statusCode': 200,
            'data': {'secret_link': href_value}
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': False,
            'error_message': str(e),
            'statusCode': 500,
            'data': {}
        }), 500
    
    finally:
        driver.quit()