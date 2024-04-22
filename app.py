import os
import json
import requests
import subprocess
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL")

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'status': True,
        'message': 'Welcome to Privnote API',
        'statusCode': 200,
        'data': []
    }), 200


@app.route('/test-note', methods=['POST'])
def test_note():
    try:
        payload = request.json
        secret_note = payload.get("secret_note")

        headers = {"Content-Type": "text/plain"}
        response = requests.post(API_BASE_URL, data=secret_note, headers=headers)

        if response.status_code == 200:
            note_url = response.text.strip()
            # entry_uuid = response.headers.get("X-Entry-Uuid")
            # entry_key = response.headers.get("X-Entry-Key")
            entry_expire = response.headers.get("X-Entry-Expire")
            
            return jsonify({
                'status': True,
                'message': 'Secret note created successfully',
                'statusCode': 200,
                'data': {
                    "note_url": note_url,
                    # "uuid": entry_uuid,
                    # "key": entry_key,
                    "expire": entry_expire
                }
            }), 200
        else:
            raise Exception("Failed to create secret note.")
        
    except json.JSONDecodeError:
        return jsonify({
            'status': False, 
            'error_message': 'Invalid JSON format', 
            'statusCode': 400, 
            'data': {}
        }), 400
        
    except Exception as e:
        return jsonify({
            'status': False,
            'error_message': str(e),
            'statusCode': 500,
            'data': {}
        }), 500


@app.route('/read-note', methods=['POST'])
def read_note():
    try:
        payload = request.json
        secret_link = payload.get("secret_link")

        response = requests.get(secret_link)

        if response.status_code == 200:
            return jsonify({
                'status': True,
                'message': 'Secret note retrieved successfully',
                'statusCode': 200,
                'data': { 'note_content': response.text }
            }), 200
        else:
            raise Exception("Failed to read secret note.")
        
    except json.JSONDecodeError:
        return jsonify({
            'status': False, 
            'error_message': 'Invalid JSON format', 
            'statusCode': 400, 
            'data': {}
        }), 400
    
    except Exception as e:
        return jsonify({
            'status': False,
            'error_message': str(e),
            'statusCode': 500,
            'data': {}
        }), 500
    

@app.route('/create-note', methods=['POST'])
def create_note():
    try:
        payload = request.json
        secret_note = payload.get("secret_note")
        
        #? Prepare the command to run
        # command = ["npx", "cryptgeon", "send", "text", secret_note] #? development command
        command = ["/usr/bin/npx", "cryptgeon", "send", "text", secret_note] #? production command
        
        #? Running the CLI command and capturing the output
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            #? Assuming the URL is in the output and needs parsing
            note_string = result.stdout.strip()  #? You may need to parse this if it includes more than the URL
            note_url = note_string.replace("Note created:\n\n", "")

            print("Here's the secret note link below")
            print(note_url)

            return jsonify({
                'status': True,
                'message': 'Secret note created successfully',
                'statusCode': 200,
                'data': {
                    "note_url": note_url
                }
            }), 200
        else:
            raise Exception("Failed to create secret note. " + result.stderr)
    
    except json.JSONDecodeError:
        return jsonify({
            'status': False, 
            'error_message': 'Invalid JSON format', 
            'statusCode': 400, 
            'data': {}
        }), 400
    
    except Exception as e:
        return jsonify({
            'status': False,
            'error_message': str(e),
            'statusCode': 500,
            'data': {}
        }), 500