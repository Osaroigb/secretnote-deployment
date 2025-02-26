import os
import json
import requests
import subprocess
from flask import Flask, request
from config import Config, logging
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from utils import build_success_response, build_error_response, is_valid_lat_lng

app = Flask(__name__)

# Use Config class to access ENVs
API_KEY = Config.WHAT3WORDS_API_KEY

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
    return build_success_response(message='Welcome to SecretNote API')
    

@app.route('/convert-to-3wa', methods=['GET'])
def convert_to_3wa():
    lat = request.args.get('lat')
    lng = request.args.get('lng')

    # Validate inputs
    if not lat or not lng:    
        logging.warning("Missing lat or lng parameter")
        return build_error_response(message="Missing lat or lng parameter")
    
    # Validate lat and lng values
    if not is_valid_lat_lng(lat, lng):
        logging.error("Invalid latitude or longitude values")
        return build_error_response(message="Invalid latitude or longitude values")

    try:
        # Construct the API URL
        url = f"https://api.what3words.com/v3/convert-to-3wa?coordinates={lat},{lng}&key={API_KEY}"

        # Make the API request
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        # Handle errors
        if response.status_code != 200:
            return build_error_response(
                message="Failed to fetch data",
                status=response.status_code,
                data=response.json()
            )
         
        return build_success_response(
            message='Converted to 3wa successfully', 
            data=response.json()
        )

    except Exception as e:
        logging.error(str(e))
        return build_error_response(
            message=str(e),
            status=500
        )
    

@app.route('/create-note', methods=['POST'])
def create_note():
    try:
        #? Retrieve query parameters
        views = request.args.get('views')
        minutes = request.args.get('minutes')
        password = request.args.get('password')

        #* Retrieve payload from POST request
        payload = request.json
        secret_note = payload.get("secret_note")

        #! Validate secret_note presence
        if not secret_note:
            return build_error_response(message='Secret note cannot be empty')
        
        #? Validate mutually exclusive query parameters
        if views and minutes:
            return build_error_response(message='Only one of "views" or "minutes" should be present, not both.')
        
        #* Prepare the command to run
        command = ["npx", "cryptgeon", "send", "text", secret_note] 

        #! Validate and handle the 'views' parameter
        if views:
            try:
                views = int(views)

                if not (1 <= views <= 10):
                    return build_error_response(message='"views" must be an integer between 1 and 10.')
                
                #? Add the views argument to the command
                command.extend(["--views", str(views)])

            except ValueError:
                return build_error_response(message='"views" must be a valid integer.')

        #* Validate and handle the 'minutes' parameter
        if minutes:
            try:
                minutes = int(minutes)

                if not (1 <= minutes <= 1440):
                    return build_error_response(message='"minutes" must be an integer between 1 and 1440.')
                
                #! Add the minutes argument to the command
                command.extend(["--minutes", str(minutes)])

            except ValueError:
                return build_error_response(message='"minutes" must be a valid integer.')

        #? Validate and handle the 'password' parameter
        if password:
            if len(password) < 12:
                return build_error_response(message='"password" must be at least 12 characters long.')
            
            #* Add the password argument to the command
            command.extend(["--password", password])

        logging.warning("here's the updated commnad below!")
        logging.info(command)

        #! Set shell=True for Windows, False for macOS/Linux
        shell_needed = True if os.name == 'nt' else False

        #? Running the CLI command and capturing the output
        result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL, shell=shell_needed)

        logging.info(f"STDOUT: {result.stdout}")
        logging.info(f"STDERR: {result.stderr}")

        if result.returncode == 0:
            #? Assuming the URL is in the output and needs parsing
            note_string = result.stdout.strip()  #? You may need to parse this if it includes more than the URL
            note_url = note_string.replace("Note created:\n\n", "")

            logging.warning("Here's the secret note link below")
            logging.info(note_url)

            return build_success_response(
                message='Secret note created successfully', 
                data={ "note_url": note_url }
            )
        else:
            raise Exception("Failed to create secret note. " + result.stderr)
    
    except json.JSONDecodeError:
        logging.error('Invalid JSON format')
        return build_error_response(message='Invalid JSON format')
    
    except Exception as e:
        logging.error(str(e))
        return build_error_response(
            message=str(e),
            status=500
        )


@app.route('/upload-file', methods=['POST'])
def upload_file():
    try:
        #* Retrieve query parameters
        views = request.args.get('views')
        minutes = request.args.get('minutes')
        password = request.args.get('password')

        #! Check if the POST request has the file part
        if 'file' not in request.files:
            return build_error_response(message='No file part in the request')

        file = request.files['file']

        if file.filename == '':
            return build_error_response(message='No selected file')

        #? Validate mutually exclusive query parameters
        if views and minutes:       
            return build_error_response(message='Only one of "views" or "minutes" should be present, not both.')

        #* Secure the filename and save it temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        #! Prepare the command to send the file using Cryptgeon
        command = ["npx", "cryptgeon", "send", "file", filepath]

        #? Validate and handle the 'views' parameter
        if views:
            try:
                views = int(views)

                if not (1 <= views <= 10):
                    return build_error_response(message='"views" must be an integer between 1 and 10.')
                
                #* Add the views argument to the command
                command.extend(["--views", str(views)])

            except ValueError:   
                return build_error_response(message='"views" must be a valid integer.')

        #! Validate and handle the 'minutes' parameter
        if minutes:
            try:
                minutes = int(minutes)

                if not (1 <= minutes <= 1440):
                    return build_error_response(message='"minutes" must be an integer between 1 and 1440.')
                
                #? Add the minutes argument to the command
                command.extend(["--minutes", str(minutes)])

            except ValueError:
                return build_error_response(message='"minutes" must be a valid integer.')

        #* Validate and handle the 'password' parameter
        if password:

            if len(password) < 12:
                return build_error_response(message='"password" must be at least 12 characters long.')
            
            #! Add the password argument to the command
            command.extend(["--password", password])

        logging.warning("here's the updated commnad below!")
        logging.info(command)
        
        #? Set shell=True for Windows, False for macOS/Linux
        shell_needed = True if os.name == 'nt' else False

        #* Run the Cryptgeon CLI command to upload the file and get the link
        result = subprocess.run(command, capture_output=True, text=True, stdin=subprocess.DEVNULL, shell=shell_needed)

        logging.info(f"STDOUT: {result.stdout}")
        logging.info(f"STDERR: {result.stderr}")

        if result.returncode == 0:
            file_string = result.stdout.strip()
            file_url = file_string.replace("Note created:\n\n", "")

            #! Clean up by removing the file after upload
            os.remove(filepath)

            logging.warning("Here's the secret file link below")
            logging.info(file_url)

            return build_success_response(
                message='File uploaded and link generated successfully', 
                data={ "file_url": file_url }
            )
        else:
            raise Exception("Failed to upload file. " + result.stderr)
        
    except RequestEntityTooLarge:
        logging.error('File size exceeds the maximum allowed limit of 11.8 MB.')
        return build_error_response(
            message='File size exceeds the maximum allowed limit of 11.8 MB.',
            status=413
        )

    except Exception as e:
        logging.error(str(e))
        return build_error_response(
            message=str(e),
            status=500
        )