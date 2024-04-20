from connector.folderoprations import *
import requests, time

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
    