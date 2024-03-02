
import dbm

from google.oauth2 import service_account
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.credentials import Credentials
from googleapiclient.errors import HttpError
import datetime
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

email="narendradukhande30@gmail.com"
file_path = "C:\\Users\\tupti\\OneDrive\\Desktop\\new Lang\\Sem4\\SwiftSynk_PythonProject\\reference_files\\test.txt"
base_drive_folder_id = "1gvh-akOM4JlkCljrtpxAGfX4dXdbfJ2n"
credentials_file_path = "C:\\Users\\tupti\\OneDrive\\Desktop\\new Lang\\Sem4\\SwiftSynk_PythonProject\\reference_files\\syncin-411107-949b882c5e98.json"

# file_path = "C:\\Projects\\SEM 4\\SwiftSynk_PythonProject\\reference_files\\test.txt"
# credentials_file_path = "C:\\Projects\\SEM 4\\SwiftSynk_PythonProject\\reference_files\\syncin-411107-949b882c5e98.json"

def getDriveService(credentials_file_path=credentials_file_path):
    SCOPES = ['https://www.googleapis.com/auth/drive']
    # Load credentials from the service account key file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file_path,
        scopes=SCOPES
    )
    
    # Build the Google Drive API service
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service


# filesToUpload=["C:\\Users\\tupti\\OneDrive\\Desktop\\new Lang\\Sem4\\SwiftSynk_PythonProject\\reference_files\\test.txt"]
# filesToUpload = ["C:\\Projects\\SEM 4\\SwiftSynk_PythonProject\\reference_files\\test.txt"]


##To upload file on drive
def upload_file_to_drive(file_path, drive_folder_id=base_drive_folder_id, credentials_file_path=credentials_file_path):
    drive_service=getDriveService(credentials_file_path)
    file_metadata = {
        'name': file_path.split("\\")[-1],
        'parents': [drive_folder_id],
    }
    print(file_metadata)
    print(os.path.splitext(file_metadata.get('name')))
    media = MediaFileUpload(file_path, resumable=True)
    request = drive_service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    )
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")
    print(f"File uploaded successfully with file ID: {response['id']}")
    # return response['id']

def upload_files_from_folder_to_drive(folder_path, drive_folder_id, credentials_path):
    for filename in os.listdir(folder_path):
        f = os.path.join(folder_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            upload_file_to_drive(f, drive_folder_id, credentials_path)
        elif(os.path.isdir(f)):
            upload_folder_to_drive(f, drive_folder_id, credentials_path)
        else:
            print("NONE")

def create_folder_in_parent_on_drive(folder_path, parent_folder_id, credentials_path):
    drive_service=getDriveService()
    folder_name=folder_path.split("\\")[-1]

    # Set the file metadata
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]  # ID of the parent folder
    }
    print(file_metadata)
    # Create the folder
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()

    print(f"Folder '{folder_name}' created successfully in folder with ID '{parent_folder_id}'.")
    return folder.get('id')

def upload_folder_to_drive(folder_path, parent_folder_id=base_drive_folder_id, credentials_path=credentials_file_path):
    new_folder_id=create_folder_in_parent_on_drive(folder_path, parent_folder_id, credentials_path)
    upload_files_from_folder_to_drive(folder_path, new_folder_id, credentials_path)

#to delete files from drive
def delete_file_from_drive(file_name, drive_folder_id=base_drive_folder_id, credentials_file_path=credentials_file_path):
    drive_service = getDriveService()
    # file_name = os.path.basename(file_path)
    query = f"name='{file_name}' and '{drive_folder_id}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields='files(id)').execute()
    files = response.get('files', [])

    if not files:
        print(f"File '{file_name}' not found in folder with ID '{drive_folder_id}'.")
        return
    file_id = files[0]['id']
    drive_service.files().delete(fileId=file_id).execute()
    print(f"File '{file_name}' deleted successfully from Google Drive.")

##to get id of the file on drive
def get_file_id(file_name, folder_id=credentials_file_path, credentials_path=credentials_file_path):

    # Search for the file in the specified folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = getDriveService().files().list(q=query, fields='files(id)').execute()
    
    # Check if the file exists in the folder
    files = response.get('files', [])
    if not files:
        print(f"File '{file_name}' not found in folder with ID '{folder_id}'.")
        return None

    # Return the ID of the first matching file
    return files[0]['id']

#to get modified time
def get_last_modified_time(file_path):
    modified_timestamp = os.path.getmtime(file_path)
    modified_datetime = datetime.datetime.fromtimestamp(modified_timestamp)
    return modified_datetime.strftime('%Y-%m-%d %H:%M:%S')

def reUpload(file_path, drive_folder_id=base_drive_folder_id, credentials_file_path=credentials_file_path):
    file_name=os.path.basename(file_path)
    if(get_file_id!=None):
        delete_file_from_drive(file_name, drive_folder_id, credentials_file_path)
    upload_file_to_drive(file_path, drive_folder_id, credentials_file_path)

def IsInternet():
    try:
        response=requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

upload_file_to_drive(file_path)



