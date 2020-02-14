import sys

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

from filetransfer import list_files
from filetransfer import upload_file
from filetransfer import download_file
from filetransfer import createDirStructure

def authenticate():
    gauth = GoogleAuth()

    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:
        # Authenticate if they're not there

        # This is what solved the issues:
        gauth.GetFlow()
        gauth.flow.params.update({'access_type': 'offline'})
        gauth.flow.params.update({'approval_prompt': 'force'})

        gauth.LocalWebserverAuth()

    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)

    return drive

def main():
    '''
    Usage:
    List Files
    main.py -l [id]
    Id here represents the folder ID. If not specified, it will default to root

    Upload File
    main.py -u srcFile destFolderID
        destFolderID: Folder ID as specified in GDrive
    Download File
    main.py -d srcFolderID destFolderPath
        srcFolderID: Folder ID as specified in GDrive

    :return:
    '''
    drive = authenticate()

    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv))

    args = sys.argv
    args.pop(0)

    option = args.pop(0)
    print(option)

    if option == "-l":
        id = "root"
        if (len(args) > 0):
            id = args.pop(0)

        list_files(id, drive)
    elif option == "-u":
        srcFile = args.pop(0)
        '''
        id = "root"

        
        print(srcFile)
        if (len(args) > 0):
            destId = args.pop(0)
            print(destId)
            if (destId is not None):
                id = destId
        '''
        #id = createDirStructure(drive)
        #print("returned = ", id)
        upload_file(srcFile, "AS", drive)

    elif option == "-d":
        id = "root"

        if (len(args) > 0):
            srcFile = args.pop(0)
            print(srcFile)
            if (srcFile is not None):
                id = srcFile

        destination = args.pop(0)
        print(srcFile)

        download_file(srcFile, destination, drive)

    elif option == "-c":
        parent_folder_id = "root"
        print("create folder")
        createDirStructure(drive)
'''
        if (len(args) > 0):
            parentId = args.pop(0)
            print(parentId)
            if (parentId is not None):
                parent_folder_id = parentId

        if (len(args) > 0):
            folder_name = args.pop(0)
        else:
            return


        create_folder(drive, parent_folder_id, folder_name)
'''

if __name__ == "__main__":
    main();