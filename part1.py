from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google drive Permission 
SCOPES = [
    "https://www.googleapis.com/auth/drive.file"
]

# locating the project folder

BASE_DIR = Path(__file__).resolve().parent

# Where is Credentials.json located
CREDENTIALS_FILE = BASE_DIR / "credentials.json"

# Where will the token.json file gonna be located
TOKEN_FILE = BASE_DIR / "token.json"

def get_drive_service() :
    #check if credentials.json is there or not

    if not CREDENTIALS_FILE.exists() : 
        raise FileNotFoundError(
            "credentials.json is missing from the project folder."
        )
    # credential is not there at the start
    creds = None

    #cheking if token.json is there from the start or not

    if TOKEN_FILE.exists() :
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES
        )

    #if the creden. file is not valid then authentication needs to be done
    if not creds or not creds.valid: 
        #if the token is expired then try to refresh 
        if creds and creds.expired and creds.refresh_token : 
            creds.refresh(Request())

    #token isn't available or can't refresh 
    #then new OAuth Login
    else : 
        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS_FILE),
            SCOPES
        )
        creds = flow.run_local_server(port = 0)

    #save authentication info's
    TOKEN_FILE.write_text(
        creds.to_json(),
        encoding = "utf-8"
    )
    #now time to create authenticated google drive API service
    drive_service = build(
        "drive",
        "v3",
        credentials=creds
    )
    return drive_service

#main program
def main():

    print("Starting Google Drive authentication...")


    try:

        drive_service = get_drive_service()

        print("\nGoogle Drive authentication successful!")

        print("Drive service is ready.")


    except Exception as error:

        print(f"\nError: {error}")


if __name__ == "__main__":
    main()

# # taking the location of the local path of the file/folder
# file_path = input("Enter The File Path: ").strip().strip('"')

# # taking the string given by the user and converting it to path object
# path = Path(file_path)

# # if the path is not absolute then combining it with the current directory
# if not path.is_absolute() : 
#     path = Path.cwd() / path 

# # normalizing the path and converting it to absolute path

# path = path.resolve()

# #checking whether the path exists or not

# if not path.exists() : 
#     print("Error: Path does not exist.")

# #if the path exist then check whether it's a file or a folder;

# elif not path.is_file() : 
#     print("Error: The given path is not a file.")

# # if the file is valid then it's to get the MIME type of the file
# else : 
#     mime_type, _ = mimetypes.guess_type(path.name)
#     # if the mime type is not found then get the generic binary type 

#     if mime_type is None :
#         mime_type = "application/octet-stream"


#     #now to upload the file we need to create a media object
#     #preparing the media for upload
#     media = MediaFileUpload(
#         str(path),
#         mimetype = mime_type,
#         resumable = True
#     )

#     #file information
#     print("\nFile is ready for upload.")

#     print(f"Name: {path.name}")
#     print(f"MIME type: {mime_type}")

#     print(f"Media object: {media}")




#     # print("\nFile found!")

#     # print(f"Full path: {path}")

#     # print(f"Name: {path.name}")

#     # print(f"Extension: {path.suffix}")

#     # print(f"MIME type: {mime_type}")

#     # # print(f"File name: {path.name}")

#     # # print(f"File extension: {path.suffix}")

#     # print(f"File name without extension: {path.stem}")

#     # print(f"Parent folder: {path.parent}")
