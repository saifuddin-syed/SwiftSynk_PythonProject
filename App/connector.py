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
from googleapiclient.http import MediaIoBaseDownload

app_email_id="pythonproject-syncin@syncin-411107.iam.gserviceaccount.com"

class User:
    def __init__(self, username, base_drive_folder_id, secondary_folder_id):
        self.username=username
        self.base_drive_folder_id=base_drive_folder_id
        self.secondary_folder_id=secondary_folder_id
        
    def modifyUser(self, Newusername, Newbase_drive_folder_id, Newsecondary_folder_id):
        self.username=Newusername
        self.base_drive_folder_id=Newbase_drive_folder_id
        self.secondary_folder_id=Newsecondary_folder_id

mainUser=User("Narendra", "1gvh-akOM4JlkCljrtpxAGfX4dXdbfJ2n", "1Osn10FfyuozwtJA4O7k8ZxPyfmd2hCPs")

file_path = "C:/Users/tupti/OneDrive/Desktop/new Lang/Sem4/SwiftSynk_PythonProject/reference_files/test.txt"
credentials_file_path = "C:\\Users\\tupti\\OneDrive\\Desktop\\new Lang\\Sem4\\SwiftSynk_PythonProject\\reference_files\\syncin-411107-949b882c5e98.json"
client_secrets_file='C:\\Users\\tupti\\OneDrive\\Desktop\\new Lang\\Sem4\\SwiftSynk_PythonProject\\reference_files\\client_secrets.json'

# username = "syedsaif78676@gmail.com"
# file_path = "C:\\Projects\\SEM 4\\SwiftSynk_PythonProject\\reference_files\\test.txt"
# base_drive_folder_id = "1rEgaGA5mofkeCf572WVRkOWIj_4sHaWm"
# credentials_file_path = "C:\\Projects\\SEM 4\\SwiftSynk_PythonProject\\reference_files\\syncin-411107-949b882c5e98.json"

def modifyUser(Newusername=mainUser.username, Newbase_drive_folder_id=mainUser.base_drive_folder_id, Newsecondary_folder_id=mainUser.secondary_folder_id):
    global username
    username=Newusername
    global base_drive_folder_id
    base_drive_folder_id=Newbase_drive_folder_id
    global secondary_folder_id
    secondary_folder_id=Newsecondary_folder_id

def modifiedUploader(username=mainUser.username):
    while True:
        if(not IsInternet()):
            continue
        files_toCheck=dbm.getFiles(username)
        for file in files_toCheck:
            if file[1]=="Paused":
                continue
            if(datetime.datetime.strptime(get_last_modified_time(file[2]), '%Y-%m-%d %H:%M:%S')>datetime.datetime.strptime(dbm.give_last_upload_time(file[2]), '%Y-%m-%d %H:%M:%S')):
                print(datetime.datetime.strptime(get_last_modified_time(file[2]), '%Y-%m-%d %H:%M:%S'),dbm.give_last_upload_time(file[2]))
                reUpload(file[2], file[4], credentials_file_path)
                print("\n\n\n")
        time.sleep(1)

def toggeleUpload(file_path, status):
    if(status=="Synced"):
        dbm.modifyFileStatus(file_path,"Paused")
    if(status=="Paused"):
        dbm.modifyFileStatus(file_path,"Synced")

def download_file_from_drive(file_id, destination_folder_path, credentials_path=credentials_file_path):
    try:
        # Load credentials from the service account key file
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/drive.readonly']
        )

        # Build the Google Drive API service
        drive_service = build('drive', 'v3', credentials=credentials)

        # Retrieve file metadata
        file_metadata = drive_service.files().get(fileId=file_id).execute()

        # Get the file name from metadata
        file_name = file_metadata['name']

        # Create the destination file path
        destination_file_path = os.path.join(destination_folder_path, file_name)

        # Download the file
        request = drive_service.files().get_media(fileId=file_id)
        with open(destination_file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        print(f"File '{file_name}' downloaded successfully to '{destination_folder_path}'")

    except Exception as e:
        print(f"Error occurred while downloading file: {e}")

def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, ['https://www.googleapis.com/auth/drive'])
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_folder(service, folder_name="SwiftSynK"):
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=folder_metadata,
                                    fields='id').execute()
    print('Folder ID: ', folder.get('id'))
    return folder.get('id')

def grant_access(service, folder_id, email=app_email_id):
    user_permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': email
    }
    request = service.permissions().create(
        fileId=folder_id,
        body=user_permission,
        fields='id',
    )
    request.execute()

# def create_state2_folder():
#     pass

# def merge_state2_folder():
#     pass

def create_state2_file(file_path):
    file_id=dbm.give_id_by_path(file_path)
    version_id=copy_file(file_id)
    dbm.insertVersion(version_id, file_id)

def getBackToVersion(file_path):
    drive_folder_id=dbm.getParentFolderid(file_path)
    version_id=dbm.getVersionID(dbm.give_id_by_path(file_path))
    delete_file_from_drive(file_path)
    id=copy_file(version_id, drive_folder_id)
    dbm.insertFile(id,file_path,get_current_time(),drive_folder_id,"Synced")

def retainVersion(filepath):
    version_id=dbm.getVersionID(dbm.give_id_by_path(file_path))
    drive_folder_id=dbm.getParentFolderid(file_path)
    delete_file_from_drive(file_path, drive_folder_id)
    dbm.deleteVersion(version_id)

def copy_file(file_id, destination_folder_id=mainUser.secondary_folder_id, credentials_path=credentials_file_path):
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=['https://www.googleapis.com/auth/drive']
    )

    drive_service = build('drive', 'v3', credentials=credentials)

    file_metadata = drive_service.files().get(fileId=file_id, fields='name').execute()
    
    copied_file = drive_service.files().copy(
        fileId=file_id,
        body={'parents': [destination_folder_id]},
        fields='id'
    ).execute()
    print(f"File '{file_metadata['name']}' copied to destination folder with ID '{destination_folder_id}'.")
    return copied_file.get('id')

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

##To upload file on drive
def upload_file_to_drive(file_path, drive_folder_id=mainUser.base_drive_folder_id, credentials_file_path=credentials_file_path):
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
    dbm.insertFile(response['id'],file_path,get_current_time(),drive_folder_id,"Synced")

def upload_files_from_folder_to_drive(folder_path, drive_folder_id, credentials_path):
    for filename in os.listdir(folder_path):
        f = folder_path+"/"+ filename
        # checking if it is a file
        if os.path.isfile(f):
            upload_file_to_drive(f, drive_folder_id, credentials_path)
        elif(os.path.isdir(f)):
            upload_folder_to_drive(f, drive_folder_id, credentials_path)
        else:
            print("NONE")

def create_folder_in_parent_on_drive(folder_path="Second space", parent_folder_id=mainUser.base_drive_folder_id, credentials_path=credentials_file_path):
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

def upload_folder_to_drive(folder_path, parent_folder_id=mainUser.base_drive_folder_id, credentials_path=credentials_file_path):
    new_folder_id=create_folder_in_parent_on_drive(folder_path, parent_folder_id, credentials_path)
    dbm.insertFolder(new_folder_id,folder_path,mainUser.username)
    upload_files_from_folder_to_drive(folder_path, new_folder_id, credentials_path)

#to delete files from drive
def delete_file_from_drive(file_name, drive_folder_id=mainUser.base_drive_folder_id, credentials_file_path=credentials_file_path, table="file"):
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
    if(table=="version"):
        dbm.deleteVersion(file_id)
        return
    if(dbm.deleteFile(file_id)==1):
        print(f"File '{file_name}' deleted successfully from Google Drive. And DB", file_id)
    print(f"File '{file_name}' deleted successfully from Google Drive.")

def delete_folder_from_drive(folder_name, drive_folder_id=mainUser.base_drive_folder_id, credentials_file_path=credentials_file_path):
    drive_service = getDriveService()
    query = f"name='{folder_name}' and '{drive_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"
    response = drive_service.files().list(q=query, fields='files(id)').execute()
    folders = response.get('files', [])

    if not folders:
        print(f"Folder '{folder_name}' not found in parent folder with ID '{drive_folder_id}'.")
        return
    folder_id = folders[0]['id']

    files_query = f"'{folder_id}' in parents and trashed=false"
    files_response = drive_service.files().list(q=files_query, fields='files(id)').execute()
    files = files_response.get('files', [])

    for file in files:
        file_id = file['id']
        drive_service.files().delete(fileId=file_id).execute()
        print(f"File with ID '{file_id}' deleted successfully.")
        
    drive_service.files().delete(fileId=folder_id).execute()
    print(f"Folder '{folder_name}' deleted successfully from Google Drive.")
    return folder_id

##to get id of the file on drive
def get_file_id(file_name, folder_id=mainUser.base_drive_folder_id, credentials_path=credentials_file_path):
    drive_service=getDriveService()
    # Search for the file in the specified folder
    query = f"name='{file_name}' and '{folder_id}' in parents and trashed=false"
    response = drive_service.files().list(q=query, fields='files(id)').execute()
    
    # Check if the file exists in the folder
    files = response.get('files', [])
    if not files:
        print(f"File '{file_name}' not found in folder with ID '{folder_id}'.")
        return None

    # Return the ID of the first matching file
    return files[0]['id']

#to get modified time
def get_last_modified_time(file_path):
    modified_timestamp = os.path.getatime(file_path)
    modified_datetime = datetime.datetime.fromtimestamp(modified_timestamp)
    return modified_datetime.strftime('%Y-%m-%d %H:%M:%S')

#to get current time
def get_current_time():
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now)
    return now

#to compare 2 string times (true if 1 is after 2)
def compare_time(time1, time2):
    time1_obj=datetime.datetime.strptime(time1[2:], '%y-%m-%d %H:%M:%S')
    time2_obj=datetime.datetime.strptime(time2[2:], '%y-%m-%d %H:%M:%S')
    return time1_obj>time2_obj

def reUpload(file_path, drive_folder_id=mainUser.base_drive_folder_id, credentials_file_path=credentials_file_path):
    # file_name=os.path.basename(file_path)
    if(get_file_id(file_path, drive_folder_id)!=None):
        delete_file_from_drive(file_path, drive_folder_id, credentials_file_path)
    upload_file_to_drive(file_path, drive_folder_id, credentials_file_path)

def IsInternet():
    try:
        response=requests.get("https://google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False
def getlogdata():
    data = dbm.logtable()
    print('db data: ',data)

    modified_data = []
    for row in data:
        modified_row = []
        timestamp = row[3]
        modified_row.append(timestamp)
        print(modified_row)
        act = row[1]
        path_email = row[2]
        ty = row[0]
        print(ty)
        if ty == 'User':
            if act == 'insert':
                desc = 'User account: '+path_email+' was added.'
                modified_row.append(desc)
            elif act == 'update':
                desc = 'User account: '+path_email+' was updated.'
                modified_row.append(desc)
            elif act == 'delete':
                desc = 'User account: '+path_email+' was removed.'
                modified_row.append(desc)
        elif ty == 'File' or 'Folder':
            if act == 'insert':
                desc = ty+': '+os.path.basename(path_email)+' was synced. '+ty+' path: '+path_email
                modified_row.append(desc)
                print("modified_row: ",modified_row)
            elif act == 'update':
                desc = ty+': '+os.path.basename(path_email)+'   was updated. '+ty+' path: '+path_email
                modified_row.append(desc)
            elif act == 'delete':
                desc = ty+': '+os.path.basename(path_email)+' was unsynced. '+ty+' path: '+path_email
                modified_row.append(desc)
        modified_data.append(tuple(modified_row))
    print('logdata: ',modified_data)
    return modified_data





