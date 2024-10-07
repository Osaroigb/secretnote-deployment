## **SecretNote API Documentation**

### **Overview**

The **SecretNote API** is a simple RESTful API built using Flask for creating, sharing, and uploading secret notes and files. The API is designed to generate anonymous secret links using Cryptgeon CLI, which can be shared with others. It supports the following functionalities:
- Create and share encrypted text notes.
- Upload files and generate secret links.
- Maximum file upload size: **11.8 MB**.

### **Base URL**
- **Base URL**: `http://127.0.0.1:3300/`

### **Endpoints Overview**

| Method | Endpoint        | Description                        |
|--------|-----------------|------------------------------------|
| GET    | `/`             | Welcome message.                   |
| POST   | `/create-note`  | Create a secret note and get a link.|
| POST   | `/upload-file`  | Upload a file and get a secret link.|

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
This endpoint allows users to create a secret note and get a link using the Cryptgeon CLI.

**Request**:
- **Endpoint**: `/create-note`
- **Method**: `POST`
- **Headers**: `Content-Type: application/json`
- **Payload**:
  ```json
  {
    "secret_note": "Your secret message"
  }
  ```

**Example**:
```bash
curl -X POST http://127.0.0.1:3300/create-note \
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

---

### **3. POST /upload-file**

**Description**:  
This endpoint allows users to upload a file and generate a secret link to access the file using the Cryptgeon CLI.  
**Note**: The maximum allowed file size is **11.8 MB**.

**Request**:
- **Endpoint**: `/upload-file`
- **Method**: `POST`
- **Headers**: `Content-Type: multipart/form-data`
- **Payload**: The request should contain a file upload.

**Example**:
```bash
curl -X POST http://127.0.0.1:3300/upload-file \
  -F "file=@/path/to/your/file.pdf"
```

**Response (Success)**:
```json
{
  "status": true,
  "message": "File uploaded and link generated successfully",
  "statusCode": 200,
  "data": {
    "note_url": "https://cryptgeon.org/note/xxxxxxxxxx"
  }
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
  If the uploaded file exceeds the 11.8 MB limit, the API will return a `413` error with the following response:
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

### **Customization and Future Improvements**
- **Expiration**:  
  Support for setting expiration times for notes or files.
  
- **Password Protection**:  
  Add an option for password protection when creating notes or uploading files.