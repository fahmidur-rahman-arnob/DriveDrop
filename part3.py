from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# GOOGLE DRIVE PERMISSION

SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]


# PROJECT FOLDER

BASE_DIR = Path(__file__).resolve().parent


# credentials.json exists or not

CREDENTIALS_FILE = BASE_DIR / "credentials.json"

# token.json file 

TOKEN_FILE = BASE_DIR / "token.json"

# GOOGLE DRIVE AUTHENTICATION function

def get_drive_service():
    # Check credentials.json

    if not CREDENTIALS_FILE.exists():

        raise FileNotFoundError(
            "credentials.json is missing from the project folder."
        )

    # Initially there are no credentials

    creds = None

    # Check if token.json already exists

    if TOKEN_FILE.exists():

        print("Existing token.json found.")

        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )


    # If credentials don't exist OR are invalid

    if not creds or not creds.valid:


        # If token expired but refresh token exists


        if creds and creds.expired and creds.refresh_token:

            print("Token expired. Refreshing token...")

            creds.refresh(Request())



        # Otherwise start a NEW Google OAuth login

        else:

            print("Starting Google OAuth login...")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE),
                SCOPES
            )

            # Starting browser-based authentication
            flow.run_local_server(
                port=0,
                open_browser=True
            )

            # IMPORTANT:
            # Get credentials FROM THE FLOW
            
            # Instead of:
            # creds = flow.run_local_server(...)
            # because in the previous version we were getting None value in to_json() this was a bug 
            # we use:
            # flow.credentials

            creds = flow.credentials



        # Making sure that the credentials were actually received

        if creds is None:

            raise RuntimeError(
                "OAuth completed, but no credentials were returned."
            )


        # Saving the credentials for future when I want to run the program.

        TOKEN_FILE.write_text(
            creds.to_json(),
            encoding="utf-8"
        )

        print("token.json created successfully.")



    # Building the google drive service

    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )


    return drive_service



# MAIN Function

def main():

    print("=" * 50)
    print("       GOOGLE DRIVE AUTHENTICATION")
    print("=" * 50)


    try:

        drive_service = get_drive_service()

        print("\nGoogle Drive authentication successful!")

        print("Drive service is ready.")


    except Exception as error:

        print(f"\nError: {error}")



# Start program


if __name__ == "__main__":

    main()