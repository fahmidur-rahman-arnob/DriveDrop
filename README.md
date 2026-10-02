# Google Drive File Uploader (DriveDrop)

A Python-based command-line application that allows users to upload local files directly to their Google Drive using the **Google Drive API** and **OAuth 2.0 authentication**.

This project was built to practice working with APIs, OAuth authentication, file handling, MIME types, and external service integration in Python.

---

## 🚀 Features

* Upload files from a local computer to Google Drive
* Accept local file paths through the terminal
* Validate whether the provided path exists
* Verify that the provided path is actually a file
* Automatically detect the file's MIME type
* Preserve the original file format during upload
* Authenticate securely using Google OAuth 2.0
* Store authentication tokens locally for future use
* Automatically refresh expired authentication tokens when possible
* Support resumable file uploads
* Return useful information about the uploaded file
* Display the Google Drive link after a successful upload
* Handle common file and API errors

---

## 🛠️ Technologies Used

* **Python**
* **Google Drive API v3**
* **OAuth 2.0**
* **Google API Python Client**
* **google-auth**
* **google-auth-oauthlib**
* **pathlib**
* **mimetypes**

---

## 📂 Project Structure

```text
google-drive-file-uploader/
│
├── part1.py
├── part3.py
├── part4.py
├── .gitignore
├── README.md
│
├── credentials.json   # Not included in GitHub
└── token.json         # Not included in GitHub
```

### File descriptions

| File               | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| `part1.py`         | Local file path validation and file information        |
| `part3.py`         | Google OAuth 2.0 authentication                        |
| `part4.py`         | Complete Google Drive uploader                         |
| `.gitignore`       | Prevents sensitive files from being uploaded to GitHub |
| `README.md`        | Project documentation                                  |
| `credentials.json` | Google OAuth client credentials — kept locally         |
| `token.json`       | Generated authentication token — kept locally          |

---

# 🔐 Authentication

This project uses **OAuth 2.0** to access Google Drive.

The application does not ask the user to provide their Google password to the Python program.

Instead, the authentication process works like this:

```text
Python Application
       ↓
credentials.json
       ↓
Google OAuth 2.0
       ↓
Browser Authentication
       ↓
User Grants Permission
       ↓
token.json
       ↓
Authenticated Drive API Service
```

The project uses the following Google Drive scope:

```python
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]
```

The `drive.file` scope provides limited access compared with unrestricted access to the entire Google Drive.

---

# ☁️ Google Cloud Setup

Before running the project, you need to configure a Google Cloud project.

## Step 1 — Create a Google Cloud Project

Create a project from the Google Cloud Console.

Example project name:

```text
DriveDrop
```

---

## Step 2 — Enable Google Drive API

Inside your Google Cloud project:

```text
APIs & Services
       ↓
Library
       ↓
Google Drive API
       ↓
Enable
```

---

## Step 3 — Configure OAuth

Configure the OAuth consent/authentication settings for the application.

For a personal development project, the application can remain in testing mode.

Add the Google account that will be used for testing as a **Test User**.

---

## Step 4 — Create OAuth Client

Create an OAuth Client ID with:

```text
Application type:
Desktop app
```

Download the generated credentials JSON file.

Rename it:

```text
credentials.json
```

Place it inside the project directory.

---

# 💻 Installation

## 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/google-drive-file-uploader.git
```

Move into the project directory:

```bash
cd google-drive-file-uploader
```

---

## 2. Create a virtual environment

```bash
python -m venv .venv
```

### Windows — PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows — Command Prompt

```cmd
.venv\Scripts\activate.bat
```

---

## 3. Install dependencies

```bash
python -m pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

---

# 🔑 Add Google Credentials

Place your downloaded OAuth credentials inside the project folder:

```text
google-drive-file-uploader/
│
├── credentials.json
├── part4.py
└── ...
```

**Do not upload `credentials.json` to GitHub.**

The `.gitignore` file already excludes it from Git tracking.

---

# ▶️ Running the Application

Run:

```bash
python part4.py
```

The application will ask for the local path of the file.

Example:

```text
Enter the full path of the file.

File path: F:\LeetCode\Palindrome_Number.py
```

The program will validate the file and detect its MIME type.

Example:

```text
File information:
Name: Palindrome_Number.py
MIME type: text/x-python
```

Then the file will be uploaded to Google Drive.

---

# 📤 Example Output

```text
==================================================
          DRIVEDROP FILE UPLOADER
==================================================

Enter the full path of the file.

File information:
Name: Palindrome_Number.py
MIME type: text/x-python

Uploading file to Google Drive...

==================================================
           UPLOAD SUCCESSFUL
==================================================

Name: Palindrome_Number.py
File ID: 1AbCdEfGhIjKlMn...
Size: 1842 bytes
MIME type: text/x-python
Drive link: https://drive.google.com/...
```

---

# 🧠 How It Works

The complete application follows this workflow:

```text
             User
               │
               ▼
        Enter File Path
               │
               ▼
        pathlib.Path()
               │
               ▼
       Validate Local File
               │
               ▼
       Detect MIME Type
               │
               ▼
        MediaFileUpload
               │
               ▼
        OAuth 2.0 Login
               │
               ▼
        Google Credentials
               │
               ▼
        Drive API Service
               │
               ▼
      files().create()
               │
               ▼
          execute()
               │
               ▼
        Google Drive
               │
               ▼
       Upload Successful
               │
               ▼
          Drive Link
```

---

# 🔍 Core Implementation

The actual upload is performed using the Google Drive API:

```python
uploaded = (
    drive_service.files()
    .create(
        body=file_metadata,
        media_body=media,
        fields="id,name,mimeType,size,webViewLink"
    )
    .execute()
)
```

The file metadata contains the original filename:

```python
file_metadata = {
    "name": path.name
}
```

The local file is prepared for upload using:

```python
media = MediaFileUpload(
    str(path),
    mimetype=mime_type,
    resumable=True
)
```

---

# 🔒 Security

Sensitive authentication files are intentionally excluded from the repository.

The `.gitignore` contains:

```gitignore
credentials.json
token.json
.venv/
__pycache__/
*.pyc
.vscode/
```

### Never commit:

```text
❌ credentials.json
❌ token.json
❌ API keys
❌ passwords
❌ private tokens
```

---

# 🧪 Error Handling

The application handles several common errors.

### File not found

```text
File error: File not found
```

### Path is not a file

```text
Input error: The supplied path is not a file.
```

### Google Drive API error

```text
Google Drive API error: ...
```

### Unexpected errors

```text
Unexpected error: ...
```

---

# 📚 What I Learned From This Project

Building this project helped me practice several important Python and backend concepts:

### Python

* `pathlib`
* File system operations
* Exception handling
* Functions
* Modules and imports
* String processing
* Object-oriented API libraries

### APIs

* REST API concepts
* API resources and methods
* Request/response workflow
* Google Drive API
* API authentication

### Authentication

* OAuth 2.0
* Access tokens
* Refresh tokens
* OAuth client credentials
* Token persistence

### File Upload

* MIME types
* `MediaFileUpload`
* Resumable uploads
* File metadata
* Upload responses

### Project Practices

* Virtual environments
* Dependency management
* `.gitignore`
* Git and GitHub
* Keeping credentials out of source control

---

# 🔮 Future Improvements

Possible improvements for future versions:

* [ ] Upload files to a specific Google Drive folder
* [ ] Create folders from the application
* [ ] Detect duplicate files
* [ ] Add upload progress indicators
* [ ] Support multiple file uploads
* [ ] Add batch upload functionality
* [ ] Add logging
* [ ] Add file size validation
* [ ] Add a graphical user interface
* [ ] Convert the application into a REST API using FastAPI
* [ ] Add authentication for API users
* [ ] Deploy the FastAPI version to a cloud platform

---

# 🎯 Project Goal

The main goal of this project was to move beyond writing standalone Python scripts and gain practical experience integrating Python with a real-world external API.

The project demonstrates how a Python application can securely authenticate with a third-party service and perform real file operations through an API.

---

## 👨‍💻 Author

**Md. Fahmidur Rahman Arnob**

Software Engineering Student
Python & Backend Development Learner

---

## ⭐ If You Find This Project Useful

Feel free to explore the repository, suggest improvements, or build your own version of the project.
