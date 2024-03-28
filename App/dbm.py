import pymysql as p

def connect():
    return p.connect(host="localhost", user="root", password='oracle',db="SwiftSynK", port=3306)

def checkLogin(email, password):
    con = connect()
    cur = con.cursor()
    print(email)
    try:
        cur.execute("SELECT password FROM user where username='{email}';".format(email=email))
        data=cur.fetchall()
        con.close()
        print("SELECT password FROM user where username='{email}';".format(email=email))
        print(data)
        if(len(data)==0):
            return 1
        elif(data[0][0]==password):
            return 0
        else:
            return 2
    except:
        con.close()
        return 3
    return 4

def insertSignup(username,email,password,folder_id):
    con = connect()
    cur = con.cursor()
    print(email)
    try:
        data=cur.fetchall()
        cur.execute("Insert into user (Email,password,Username,base_folder_id) values ('{email}','{password}','{username}','{folder_id}');".format(email=email, password=password, username=username, folder_id=folder_id))
        print(data)
        if(len(password)>8):
            return 1
        else:
            return 0
    
    except:
        con.close()
        return 2
    return 3


def is_folder_already_added(path):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM folder where folder_path='{folder_path}';".format(folder_path=path))
        data=cur.fetchall()
        con.close()
        print(data)
        if(len(data)==0):
            return False
        return True
    except:
        con.close()
        return False
    return False

def file_already_added(path):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("SELECT * FROM file where filepath='{filepath}';".format(filepath=path))
        data=cur.fetchall()
        con.close()
        print(data)
        if(len(data)==0):
            return False
        return True
    except:
        con.close()
        return False
    return False

def providePaths(base_folder_id, email):
    con=connect()
    cur=con.cursor()
    data=[[], []]
    try:
        cur.execute("select folder_path from folder where email='{email}'and folder_path not in ('Base', 'second');".format(email=email))
        data1=cur.fetchall()
        print(data1)
        con.close()
    except Exception as e:
        print(e)
        con.close()
        print("select folder_path from folder where email='{email}'and folder_path not in ('Base');".format(email=email))
        print("Error to get folders")
        return data
    
    con=connect()
    cur=con.cursor()
    try:
        cur.execute("select filepath from file where folder_id='{base_folder_id}';".format(base_folder_id=base_folder_id))
        data2=cur.fetchall()
        print(data2)
        con.close()
    except Exception as e:
        print(e)
        con.close()
        print("select filepath from file where folder_id='{base_folder_id}';".format(base_folder_id=base_folder_id))
        print("Error to get files")
        return data

    for i in data1:
        data[0].append(i[0])
    for i in data2:
        data[1].append(i[0])
    return data

def give_id_by_path(path):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT file_id FROM file where filepath='{file_path}';".format(file_path=path))
    data=cur.fetchall()
    con.commit()
    con.close()
    print("hii", data)
    if(len(data)==0):
        return ""
    return data[0][0]

def getParentFolderid(file_path):
    con = connect()
    cur = con.cursor()
    cur.execute("select folder_id from file where filepath = '{file_path}';".format(file_path=file_path))
    con.commit()
    con.close()
    return 1

def getVersion(file_id):
    con = connect()
    cur = con.cursor()
    cur.execute("select last_version_id from lastVersions where main_file_id = '{file_id}';".format(file_id=file_id))
    con.commit()
    con.close()
    return 1

def give_last_upload_time(file_path):
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT upload_time FROM file where filepath='{file_path}';".format(file_path=file_path))
    data=cur.fetchall()
    con.commit()
    con.close()
    print("hii", data)
    if(len(data)==0):
        return ""
    return data[0][0]

def getFolders():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM folder;")
    data=cur.fetchall()
    con.commit()
    con.close()
    print(data)
    return data

def getFiles():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM file;")
    data=cur.fetchall()
    con.commit()
    con.close()
    print(data)
    return data

def getUsers():
    con = connect()
    cur = con.cursor()
    cur.execute("SELECT * FROM user;")
    data=cur.fetchall()
    con.commit()
    con.close()
    print(data)
    return data

def insertUser(email,password,username,folder_id, state_folder_id):
    con = connect()
    cur = con.cursor()
    cur.execute("Insert into user (Email,password,Username,base_folder_id) values ('{email}','{password}','{username}','{folder_id}', '{state_folder_id}');".format(email=email, password=password, username=username, folder_id=folder_id, state_folder_id=state_folder_id))
    con.commit()
    con.close()
    return 1

def insertFolder(folder_id,folder_path,email):
    con = connect()
    cur = con.cursor()
    cur.execute("Insert into folder (folder_id,folder_path,Email) values ('{folder_id}','{folder_path}','{email}');".format(folder_id=folder_id, folder_path=folder_path, email=email))
    con.commit()
    con.close()
    return 1

def insertFile(file_id,filepath,upload_time,folder_id,status):
    con = connect()
    cur = con.cursor()
    cur.execute("Insert into file (file_id,filepath,upload_time,folder_id,Status) values ('{file_id}','{filepath}','{upload_time}','{folder_id}','{status}');".format(file_id=file_id, filepath=filepath, upload_time=upload_time, folder_id=folder_id, status=status))
    con.commit()
    con.close()
    return 1

def insertVersion(version_file_id,file_id):
    con = connect()
    cur = con.cursor()
    cur.execute("Insert into lastVersions (last_version_id, main_file_id) values ('{last_version_id}','{main_file_id}');".format(last_version_id=version_file_id,main_file_id=file_id))
    con.commit()
    con.close()
    return 1

def deleteUser(dEmail):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("Delete from User where Email = '{dEmail}';".format(dEmail=dEmail))
        con.commit()
    except:
        con.close()
        return 0
    con.close()
    return 1

def deleteFolder(dFolder_id):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("Delete from file where folder_id = '{dFolder_id}';".format(dFolder_id=dFolder_id))
        try:
            cur.execute("Delete from folder where folder_id = '{dFolder_id}';".format(dFolder_id=dFolder_id))
            con.commit()
            con.close()
            return 1
        except Exception as e:
            print("error occured")
            print(e)
            con.close()
            return 0
    except:
        print("error occured")
        print(e)
        con.close()
        return 0

def deleteFile(dFile_id):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("Delete from file where file_id = '{dFile_id}';".format(dFile_id=dFile_id))
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        con.close()
        return 0

def deleteVersion(dFile_id):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("Delete from lastVersions where last_version_id = '{dFile_id}';".format(dFile_id=dFile_id))
        con.commit()
        con.close()
        return 1
    except Exception as e:
        print(e)
        con.close()
        return 0

def modifyUser(mpassword,mUsername,memail):
    con = connect()
    cur = con.cursor()
    cur.execute("Update User set password ='{mpassword}', Username = '{mUsername}' where email = '{memail}';".format(mpassword=mpassword, mUsername=mUsername, memail=memail))
    con.commit()
    con.close()
    return 1

def modifyFolder(mfolder_path,mfolder_id):
    con = connect()
    cur = con.cursor()
    cur.execute("Update folder set folder_path = '{mfolder_path}' where folder_id = '{mfolder_id}';".format(mfolder_id=mfolder_id, mfolder_path=mfolder_path))
    con.commit()
    con.close()
    return 1

def modifyFile(mfilepath,mfile_id,mupload_time,mStatus):
    con = connect()
    cur = con.cursor()
    cur.execute("Update file set filepath = '{mfilepath}', upload_time = '{mupload_time}', Status = '{mStatus}' where file_id = '{mfile_id}';".format(mfilepath=mfilepath, mupload_time=mupload_time, mStatus=mStatus, mfile_id=mfile_id))
    con.commit()
    con.close()
    return 1

def modifyFileStatus(mfilepath,mStatus):
    con = connect()
    cur = con.cursor()
    cur.execute("Update file set Status = '{mStatus}' where filepath = '{mfilepath}';".format(mfilepath=mfilepath, mStatus=mStatus))
    con.commit()
    con.close()
    return 1

# def logfiles(logid):
#     con = connect()
#     cur = con.cursor()
#     cur.execute("select filepath from file where file_id = '{logid}';".format(logid=logid))
#     file_data = cur.fetchall()
#     print("Fetched file path:", file_data)
#     con.close()
#     if file_data:
#         file_path = file_data[0][0]
#         return file_path
#     else:
#         return None

# def logfolders(logid):
#     con = connect()
#     cur = con.cursor()
#     cur.execute("select folder_path from folder where folder_id = '{logid}';".format(logid=logid))
#     folder_data = cur.fetchall()
#     con.close()

#     if folder_data:
#         folder_path = folder_data[0][0]
#         return folder_path
#     else:
#         return None


# def logusers(logemail):
#     con = connect()
#     cur = con.cursor()
#     cur.execute("select username from user where email = '{logemail}';".format(logemail=logemail))
#     uname = cur.fetchall()
#     con.close()
#     if uname:
#         username = uname[0][0]
#         return username
#     else:
#         return None

def logtable():
    con = connect()
    cur = con.cursor()
    cur.execute("select * from logtable;")
    data = cur.fetchall()
    con.commit()
    con.close()
    return data