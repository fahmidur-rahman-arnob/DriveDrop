import mimetypes
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# GOOGLE DRIVE PERMISSION

SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]

# PROJECT DIRECTORY

BASE_DIR = Path(__file__).resolve().parent

# GOOGLE OAUTH FILES

CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"

# GOOGLE DRIVE AUTHENTICATION

def get_drive_service():
    # Check credentials.json

    if not CREDENTIALS_FILE.exists():

        raise FileNotFoundError(
            "credentials.json is missing from the project folder."
        )

    # Initially no credentials

    creds = None

    # Check token.json

    if TOKEN_FILE.exists():

        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )


    # If credentials don't exist or aren't valid

    if not creds or not creds.valid:

        # Refresh expired token

        if creds and creds.expired and creds.refresh_token:

            print("Refreshing expired token...")

            creds.refresh(Request())

        # Start new OAuth authentication

        else:

            print("Starting Google OAuth login...")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )

            flow.run_local_server(
                port=0,
                open_browser=True
            )

            # Get credentials from the OAuth flow
            creds = flow.credentials


        # Make sure credentials exist

        if creds is None:

            raise RuntimeError(
                "OAuth completed, but credentials were not received."
            )

        # Save credentials

        TOKEN_FILE.write_text(
            creds.to_json(),
            encoding="utf-8"
        )


    # CREATE AUTHENTICATED DRIVE SERVICE

    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )


    return drive_service

# FILE UPLOAD FUNCTION

def upload_file(drive_service, file_path):
    # Convert user input into Path object

    path = Path(file_path).expanduser()

    # Convert relative path into absolute path

    if not path.is_absolute():

        path = Path.cwd() / path

    # Resolve the path


    path = path.resolve()


    # Check whether file exists

    if not path.exists():

        raise FileNotFoundError(
            f"File not found: {path}"
        )



    # Make sure the path is a file

    if not path.is_file():

        raise ValueError(
            "The supplied path is not a file."
        )

    # MIME TYPE DETECTION

    mime_type, _ = mimetypes.guess_type(
        path.name
    )


    # Fallback MIME type

    if mime_type is None:

        mime_type = "application/octet-stream"


    print("\nFile information:")
    print(f"Name: {path.name}")
    print(f"MIME type: {mime_type}")

    # FILE METADATA

    file_metadata = {
        "name": path.name
    }


    # PREPARE FILE FOR UPLOAD

    media = MediaFileUpload(
        str(path),
        mimetype=mime_type,
        resumable=True
    )


    print("\nUploading file to Google Drive...")

    # ACTUAL GOOGLE DRIVE UPLOAD

    uploaded = (
        drive_service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id,name,mimeType,size,webViewLink"
        )
        .execute()
    )

    # DISPLAY UPLOAD RESULT

    print("\n" + "=" * 50)
    print("           UPLOAD SUCCESSFUL")
    print("=" * 50)

    print(f"Name: {uploaded.get('name')}")
    print(f"File ID: {uploaded.get('id')}")
    print(f"Size: {uploaded.get('size', 'Not returned')} bytes")
    print(f"MIME type: {uploaded.get('mimeType')}")
    print(f"Drive link: {uploaded.get('webViewLink')}")


    return uploaded



# MAIN PROGRAM

def main():

    print("=" * 50)
    print("          DRIVEDROP FILE UPLOADER")
    print("=" * 50)


    try:

        # Authenticate with Google Drive

        drive_service = get_drive_service()
        # Ask user for local file path

        print("\nEnter the full path of the file.")

        print(
            r'Example: C:\Users\Arnob\Documents\notes.docx'
        )


        file_path = input("\nFile path: ").strip()


        # Remove quotes if user pasted quoted path

        file_path = file_path.strip('"')

        # Upload file

        upload_file(
            drive_service,
            file_path
        )

    # ERROR HANDLING

    except FileNotFoundError as error:

        print(f"\nFile error: {error}")


    except ValueError as error:

        print(f"\nInput error: {error}")


    except HttpError as error:

        print(f"\nGoogle Drive API error: {error}")


    except Exception as error:

        print(f"\nUnexpected error: {error}")


# =========================================================
# RUN PROGRAM
# =========================================================

if __name__ == "__main__":

    main()