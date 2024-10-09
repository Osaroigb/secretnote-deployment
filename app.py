# import requests
# from dotenv import load_dotenv

# load_dotenv()
# API_BASE_URL = os.getenv("API_BASE_URL")

import os
import json
import subprocess
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

app = Flask(__name__)

#? Set an upload folder for saving the file temporarily
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#* Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

#! Set a maximum file upload size (11.8 MB = 11.8 * 1024 * 1024 bytes)
app.config['MAX_CONTENT_LENGTH'] = 11.8 * 1024 * 1024


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'status': True,
        'message': 'Welcome to SecretNote API',
        'statusCode': 200,
        'data': []
    }), 200


# @app.route('/test-note', methods=['POST'])
# def test_note():
#     try:
#         payload = request.json
#         secret_note = payload.get("secret_note")

#         headers = {"Content-Type": "text/plain"}
#         response = requests.post(API_BASE_URL, data=secret_note, headers=headers)

#         if response.status_code == 200:
#             note_url = response.text.strip()
#             # entry_uuid = response.headers.get("X-Entry-Uuid")
#             # entry_key = response.headers.get("X-Entry-Key")
#             entry_expire = response.headers.get("X-Entry-Expire")
            
#             return jsonify({
#                 'status': True,
#                 'message': 'Secret note created successfully',
#                 'statusCode': 200,
#                 'data': {
#                     "note_url": note_url,
#                     # "uuid": entry_uuid,
#                     # "key": entry_key,
#                     "expire": entry_expire
#                 }
#             }), 200
#         else:
#             raise Exception("Failed to create secret note.")
        
#     except json.JSONDecodeError:
#         return jsonify({
#             'status': False, 
#             'error_message': 'Invalid JSON format', 
#             'statusCode': 400, 
#             'data': {}
#         }), 400
        
#     except Exception as e:
#         return jsonify({
#             'status': False,
#             'error_message': str(e),
#             'statusCode': 500,
#             'data': {}
#         }), 500


# @app.route('/read-note', methods=['POST'])
# def read_note():
#     try:
#         payload = request.json
#         secret_link = payload.get("secret_link")

#         response = requests.get(secret_link)

#         if response.status_code == 200:
#             return jsonify({
#                 'status': True,
#                 'message': 'Secret note retrieved successfully',
#                 'statusCode': 200,
#                 'data': { 'note_content': response.text }
#             }), 200
#         else:
#             raise Exception("Failed to read secret note.")
        
#     except json.JSONDecodeError:
#         return jsonify({
#             'status': False, 
#             'error_message': 'Invalid JSON format', 
#             'statusCode': 400, 
#             'data': {}
#         }), 400
    
#     except Exception as e:
#         return jsonify({
#             'status': False,
#             'error_message': str(e),
#             'statusCode': 500,
#             'data': {}
#         }), 500
    

@app.route('/create-note', methods=['POST'])
def create_note():
    try:
        payload = request.json
        secret_note = payload.get("secret_note")
        
        #? Prepare the command to run
        command = ["npx", "cryptgeon", "send", "text", secret_note] 
        
        #? Running the CLI command and capturing the output
        # result = subprocess.run(command, capture_output=True, text=True)
        # result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL)

        #? Set shell=True for Windows, False for macOS/Linux
        shell_needed = True if os.name == 'nt' else False

        #? Running the CLI command and capturing the output
        result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL, shell=shell_needed)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

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
    

@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        #! Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({
                'status': False,
                'error_message': 'No file part in the request',
                'statusCode': 400,
                'data': {}
            }), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'status': False,
                'error_message': 'No selected file',
                'statusCode': 400,
                'data': {}
            }), 400

        #? Secure the filename and save it temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #* Prepare the command to send the file using Cryptgeon
        command = ["npx", "cryptgeon", "send", "file", filepath]

        #! Run the Cryptgeon CLI to upload the file and get the link
        # result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL)

        #? Set shell=True for Windows, False for macOS/Linux
        shell_needed = True if os.name == 'nt' else False

        #? Running the CLI command and capturing the output
        result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL, shell=shell_needed)

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        if result.returncode == 0:
            file_string = result.stdout.strip()
            file_url = file_string.replace("Note created:\n\n", "")

            #? Clean up by removing the file after upload
            os.remove(filepath)

            print("Here's the secret file link below")
            print(file_url)

            return jsonify({
                'status': True,
                'message': 'File uploaded and link generated successfully',
                'statusCode': 200,
                'data': {
                    "file_url": file_url
                }
            }), 200
        else:
            raise Exception("Failed to upload file. " + result.stderr)
        
    except RequestEntityTooLarge:
        return jsonify({
            'status': False,
            'error_message': 'File size exceeds the maximum allowed limit of 11.8 MB.',
            'statusCode': 413,
            'data': {}
        }), 413

    except Exception as e:
        return jsonify({
            'status': False,
            'error_message': str(e),
            'statusCode': 500,
            'data': {}
        }), 500