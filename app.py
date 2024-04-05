import os
import time
from dotenv import load_dotenv
from driver import setup_chrome_driver
from flask import Flask, request, jsonify
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

app = Flask(__name__)

@app.route('/create-secret-note', methods=['POST'])
def create_secret_note():
    driver = setup_chrome_driver()

    try:
        secret_note = request.json.get("secret_note")
        privnote_url = os.getenv("PRIV_URL", "default_url")        
        driver.get(privnote_url)

        textarea = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "note_text"))
        )

        textarea.clear()
        textarea.send_keys(secret_note)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "encrypt_note"))
        )

        button.click()

        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "note_link_input"))
        )
        input_content = input_element.get_attribute("value")

        print('secret note link')
        print(input_content)

        time.sleep(2)

        current_url = driver.current_url
        print(f"The current URL is: {current_url}")
        
        return jsonify({
            'status': True,
            'message': 'Secret note link retrieved successfully',
            'statusCode': 200,
            'data': {'secret_link': current_url}
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