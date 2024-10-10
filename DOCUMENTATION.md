## **SecretNote API Documentation**

### **Overview**

The **SecretNote API** is a simple RESTful API built using Flask for creating, sharing, and uploading secret notes and files. The API is designed to generate anonymous secret links using the Cryptgeon CLI, which can be shared with others. It supports the following functionalities:

- Create and share encrypted text notes.
- Upload files and generate secret links.
- Set notes/files to expire after a specified number of views or a specific time duration.
- Protect notes/files with a custom password.
- Maximum file upload size: **11.8 MB**.

### **Base URL**
- **Base URL**: `http://127.0.0.1:3300/`

---

### **Endpoints Overview**

| Method | Endpoint        | Description                                      |
|--------|-----------------|--------------------------------------------------|
| GET    | `/`             | Welcome message.                                 |
| POST   | `/create-note`  | Create a secret note and get a link.             |
| POST   | `/upload-file`  | Upload a file and get a secret link.             |

---

### **1. GET /**

**Description**:  
Returns a welcome message and API status.

**Request**:  
```bash
GET /
```

**Response**:
```json
{
  "status": true,
  "message": "Welcome to SecretNote API",
  "statusCode": 200,
  "data": []
}
```

---

### **2. POST /create-note**

**Description**:  
This endpoint allows users to create a secret note and get a link using the Cryptgeon CLI. The note can have advanced features like expiration after a certain number of views or after a specific time duration (in minutes). You can also protect the note with a custom password.

**Advanced Features**:
- **views** (optional): The note will expire after `n` views. The maximum value for `n` is 10.
- **minutes** (optional): The note will expire after `n` minutes. The maximum value for `n` is 1440 (24 hours).
- **password** (optional): Protect the note with a custom password (minimum length of 12 characters).
  
**Note**: Either `views` or `minutes` can be specified, but **not both**. If both are provided, the request will fail with a validation error.

**Request**:
- **Endpoint**: `/create-note`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Query Parameters** (optional):
  - `views`: Integer (1-10).
  - `minutes`: Integer (1-1440).
  - `password`: String (minimum 12 characters).
- **Payload**:
  ```json
  {
    "secret_note": "Your secret message"
  }
  ```

**Examples**:
1. **Create a note with 5 views**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/create-note?views=5" \
   -H "Content-Type: application/json" \
   -d '{"secret_note": "Your secret message"}'
   ```

2. **Create a note that expires after 30 minutes**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/create-note?minutes=30" \
   -H "Content-Type: application/json" \
   -d '{"secret_note": "Your secret message"}'
   ```

3. **Create a note with a custom password**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/create-note?password=myStrongPass123" \
   -H "Content-Type: application/json" \
   -d '{"secret_note": "Your secret message"}'
   ```

**Response**:
```json
{
  "status": true,
  "message": "Secret note created successfully",
  "statusCode": 200,
  "data": {
    "note_url": "https://cryptgeon.org/note/xxxxxxxxxx"
  }
}
```

**Errors**:
- **If both `views` and `minutes` are provided**:
  ```json
  {
    "status": false,
    "error_message": "Only one of 'views' or 'minutes' should be present, not both.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `views` is not between 1 and 10**:
  ```json
  {
    "status": false,
    "error_message": "'views' must be an integer between 1 and 10.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `minutes` is not between 1 and 1440**:
  ```json
  {
    "status": false,
    "error_message": "'minutes' must be an integer between 1 and 1440.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `password` is shorter than 12 characters**:
  ```json
  {
    "status": false,
    "error_message": "'password' must be at least 12 characters long.",
    "statusCode": 400,
    "data": {}
  }
  ```

---

### **3. POST /upload-file**

**Description**:  
This endpoint allows users to upload a file and generate a secret link to access the file using the Cryptgeon CLI. You can also apply advanced features such as expiration by views, expiration by time, and password protection.

**Advanced Features**:
- **views** (optional): The file link will expire after `n` views. The maximum value for `n` is 10.
- **minutes** (optional): The file link will expire after `n` minutes. The maximum value for `n` is 1440 (24 hours).
- **password** (optional): Protect the file with a custom password (minimum length of 12 characters).

**Note**: Either `views` or `minutes` can be specified, but **not both**.

**Request**:
- **Endpoint**: `/upload-file`
- **Method**: `POST`
- **Headers**: `Content-Type: multipart/form-data`
- **Query Parameters** (optional):
  - `views`: Integer (1-10).
  - `minutes`: Integer (1-1440).
  - `password`: String (minimum 12 characters).
- **Payload**: The request must contain a file upload.

**Examples**:
1. **Upload a file with 5 views**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/upload-file?views=5" \
   -F "file=@/path/to/your/file.pdf"
   ```

2. **Upload a file that expires after 30 minutes**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/upload-file?minutes=30" \
   -F "file=@/path/to/your/file.pdf"
   ```

3. **Upload a file with a custom password**:
   ```bash
   curl -X POST "http://127.0.0.1:3300/upload-file?password=myStrongPass123" \
   -F "file=@/path/to/your/file.pdf"
   ```

**Response (Success)**:
```json
{
  "status": true,
  "message": "File uploaded and link generated successfully",
  "statusCode": 200,
  "data": {
    "file_url": "https://cryptgeon.org/note/xxxxxxxxxx"
  }
}
```

**Errors**:
- **If both `views` and `minutes` are provided**:
  ```json
  {
    "status": false,
    "error_message": "Only one of 'views' or 'minutes' should be present, not both.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `views` is not between 1 and 10**:
  ```json
  {
    "status": false,
    "error_message": "'views' must be an integer between 1 and 10.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `minutes` is not between 1 and 1440**:
  ```json
  {
    "status": false,
    "error_message": "'minutes' must be an integer between 1 and 1440.",
    "statusCode": 400,
    "data": {}
  }
  ```

- **If `password` is shorter than 12 characters**:
  ```json
  {
    "status": false,
    "error_message": "'password' must be at least 12 characters long.",
    "statusCode": 400,
    "data": {}
  }
  ```

**Response (File Too Large)**:
```json
{
  "status": false,
  "error_message": "File size exceeds the maximum allowed limit of 11.8 MB.",
  "statusCode": 413,
  "data": {}
}
```

---

### **Error Handling**

- **413 Payload Too Large**:  
  If the uploaded file exceeds the 11.8 MB limit, the API will return a `413` error:
  ```json


  {
    "status": false,
    "error_message": "File size exceeds the maximum allowed limit of 11.8 MB.",
    "statusCode": 413,
    "data": {}
  }
  ```

- **500 Internal Server Error**:  
  If any server-side error occurs during the execution of the command, a generic error response is returned:
  ```json
  {
    "status": false,
    "error_message": "Failed to upload file. [error details]",
    "statusCode": 500,
    "data": {}
  }
  ```

---

### **Environment Setup**

Ensure that your environment is properly set up with the following:

1. **Install Flask and Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Install Cryptgeon CLI**:
   You can install the Cryptgeon CLI globally:
   ```bash
   npm -g install cryptgeon
   ```

---

### **Testing the API**

You can use tools like [Postman](https://www.postman.com/) or [curl](https://curl.se/) to interact with these endpoints. Refer to the [API documentation](https://documenter.getpostman.com/view/23691550/2sA358c5dQ) for detailed endpoint information.
For file uploads, ensure the file size does not exceed **11.8 MB**.

---

### **Advanced Customization and Improvements**

- **Expiration**:  
  Support for setting expiration times for notes or files based on views or minutes.

- **Password Protection**:  
  The option to add password protection when creating notes or uploading files has been added.