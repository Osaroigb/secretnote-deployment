# SecretNote API

The SecretNote API is a custom RESTful API built with Flask for creating and reading secret notes. Each note is created anonymously and can be accessed through a unique URL. The API is designed with simplicity in mind, focusing on the core functionality of managing secret notes.

## Features

- Creation of secret notes with a POST request
- Reading of secret notes through a unique URL
- Simple and RESTful endpoints
- Consistent error and success response formats

## Getting Started

### Prerequisites

Before you start, make sure you have installed:

- Python 3.8 or later
- pip (Python package manager)
- Virtualenv (optional, for creating isolated Python environments)

### Installation

1. **Clone the Repository**

   Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/Osaroigb/secretnote-deployment.git
   cd secretnote-deployment
   ```

2. **Set Up a Virtual Environment (Optional)**

   If you're using virtualenv, set up a new environment:

   ```bash
   python -m venv env
   ```

   Activate the virtual environment:

   - On macOS/Linux:
     ```bash
     source env/bin/activate
     ```
   - On Windows:
     ```bash
     env\Scripts\activate
     ```

3. **Install Dependencies**

   Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables Setup**

   You will find a `.env.example` file in the root directory. Make a copy of this file and rename it to `.env`. This file will be used to store your environment variables securely.

   ```bash
   cp .env.example .env  # Unix/MacOS
   copy .env.example .env  # Windows
   ```

5. **Update `.env` File**

   Open the `.env` file and fill in other environment variables


### Running the API Locally

1. **Start the Flask Development Server**

   Execute the following command to run the Flask server:

   ```bash
   python run.py
   ```

   By default, Flask will serve the API on `http://127.0.0.1:3300/`.

2. **Accessing the API Endpoints**

   The API has two main endpoints:

   - Create a secret note: `POST /create-secret-note`
     - Endpoint to create a [secretnote link](https://cryptgeon.org/note/7n5v5b6S6I5h5v7I516X4b5V5W64796O6Q4B6y4I7D5G6g7a65485B4g6K7G6I4j#1fb8dd65aca51e2c08e06c5e966adba2d1810c67b719f1fb749f2ed7b40c356f) to a secret note. The request JSON should contain the `secret_note`. An example link https://cryptgeon.org/note/7n5v5b6S6I5h5v7I516X4b5V5W64796O6Q4B6y4I7D5G6g7a65485B4g6K7G6I4j#1fb8dd65aca51e2c08e06c5e966adba2d1810c67b719f1fb749f2ed7b40c356f

   You can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to interact with these endpoints. Refer to the [API documentation](https://documenter.getpostman.com/view/23691550/2sA358c5dQ) for detailed endpoint information.

   
## Customization

This Flask API is designed to be simple and focused on managing secret notes. However, you can extend or customize it by adding more functionalities, such as note expiration, user authentication, and more sophisticated error handling.

## License

This project is open-sourced under the Mozilla Public License. See the [LICENSE](LICENSE) file for more details.