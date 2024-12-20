from connector.fileoprations import *
from googleapiclient.http import MediaIoBaseDownload

def toggeleUpload(file_path, status):
    if(status=="Synced"):
        dbm.modifyFileStatus(file_path,"Paused")
    if(status=="Paused"):
        dbm.modifyFileStatus(file_path,"Synced")

def download_file_from_drive(file_id, credentials_path=credentials_file_path):
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
        destination_file_path = os.path.join("/", file_name)

        # Download the file
        request = drive_service.files().get_media(fileId=file_id)
        with open(destination_file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

        print(f"File '{file_name}' downloaded successfully to '{file_name}'")

    except Exception as e:
        print(f"Error occurred while downloading file: {e}")

def create_state2_file(file_path):
    file_id=dbm.give_id_by_path(file_path)
    version_id=copy_file(file_id)
    dbm.insertVersion(version_id, file_id)

# copy last file version in main and removes from 2 state
def getBackToVersion(file_path):
    # print("Get back to function")
    drive_folder_id=dbm.getParentFolderid(file_path)
    mainFileID=dbm.give_id_by_path(file_path)
    version_id=dbm.getVersion(mainFileID)
    id=copy_file(version_id, drive_folder_id)
    delete_file_from_drive(file_path, mainUser.secondary_folder_id, "version")
    delete_file_from_driveUsingFileID(mainFileID)
    dbm.deleteFile(mainFileID)
    dbm.insertFile(id,file_path,get_current_time(),drive_folder_id,"Synced")

#delete last version and removes 2 state
def retainVersion(file_path):
    delete_file_from_drive(file_path, mainUser.secondary_folder_id, "version")

#Update last version
def updateVersion(file_path):
    delete_file_from_drive(file_path, mainUser.secondary_folder_id, "version")
    drive_folder_id=dbm.getParentFolderid(file_path)
    mainFileID=dbm.give_id_by_path(file_path)
    id=copy_file(mainFileID, mainUser.secondary_folder_id)
    dbm.insertVersion(id, mainFileID)

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
