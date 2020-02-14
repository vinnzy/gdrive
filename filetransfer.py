import shutil
import datetime
import glob
import os

def get_files(path):
    return glob.glob(path + "/*")


def upload_file(srcPath, destination, drive):
	'''
	:param srcPath: Path to the directory that needs to be uploadded
	:param destination: This is the directory ID in GDrive. By default root is taken if none is specified
	:param drive: GDrive instance
	:return:
	'''

	files = get_files(srcPath)
	for file in files:
		#First create a directory path if it does not exist
		filename = '.'.join(file.split('.')[:-2])

		fTitle = os.path.basename(file)
		try:
			destination = createDirStructure(drive, filename)
		except Exception:
			pass

		file_metadata = {'title': fTitle, "parents": [{"id": destination, "kind": "drive#childList"}],'resumable': True}
		try:
			new_file = drive.CreateFile(file_metadata)
			# Read file and set it as a content of this instance.
			new_file.SetContentFile(file)
			print("file = ", file)
			drive.auth.service.files().insert(body=file_metadata,media_body=file).execute()
			#new_file.Upload()  # Upload the file.
			os.remove(file)
		except Exception as e:
			print("failed to upload =", file)
			print(e)
			pass

	print("File uploaded to ", destination)


def list_files(id, drive):
	'''

	:param id: GDrive id of the directory
	:param drive: GDrive instance
	:return:
	'''
	# Auto-iterate through all files that matches this query
	query = {'q': "'" + id + "'" + " in parents and trashed=false"}
	file_list = drive.ListFile(query).GetList()
	for file1 in file_list:
		print('title: %s, id: %s' % (file1['title'], file1['id']))


def download_file(srcFile, destinationFolder, drive):

	fileObj = drive.CreateFile({'id': srcFile})
	fileObj.GetContentFile('HappyFort.ods')

	fname = fileObj['title']

	print(fname)
	shutil.move(fname, destinationFolder)

def create_folder(drive, parent_folder_id, folder_name):
    # type: (GoogleDrive, str, str) -> str
    """Create a folder at the given folder id location with a folder name.

    Args:
        drive: Auth object.
        parent_folder_id: folder location you would like this folder created.
        folder_name: name of the folder.

    Returns:
        folder_id: of this newly created folder.
    """
    try:
        folder = drive.CreateFile(dict(
            title=folder_name,
            parents=[dict(id=parent_folder_id)],
            mimeType="application/vnd.google-apps.folder"
        ))
    except Exception as e:
        raise('problem creating folder')

    try:
        folder.Upload()
    except Exception as e:
        pass

    print(folder['id'])

    return folder['id']

import dateutil.parser as dparser
def createDirStructure(drive, filename):
	'''
	Create a Dir struture in Gdrive
	:param drive:
	:param parent_folder_id:
	:param folder_name:
	:return:
	'''
	try:
		res = filename.partition("_")[2]
		print(res)

		dt = (dparser.parse(res, fuzzy=True))
		print(dt.day, " ", dt.month, " ", dt.year, " ", dt.date(), " ", dt.strftime("%B"))

		folder_id = isFileExists(drive, "root", str(dt.year))

		if folder_id is None:
			folder_id = create_folder(drive, "root", str(dt.year))

		print(folder_id)
		temp_folder_id = isFileExists(drive, folder_id, str(dt.strftime("%B")))
		if temp_folder_id is None:
			folder_id = create_folder(drive, folder_id, str(dt.strftime("%B")))
		else:
			folder_id = temp_folder_id
		print(folder_id)
		temp_folder_id = isFileExists(drive, folder_id, str(dt.date()))
		print("temp_folder_id = ", temp_folder_id)
		if temp_folder_id is None:
			folder_id = create_folder(drive, folder_id, str(dt.date()))
		else:
			folder_id = temp_folder_id

		return folder_id

		raise Exception('general exceptions not caught by specific handling')
	except Exception:
		print("nothing")


def isFileExists(drive, id, folder_name):
	#Let us first create a year directory
	#first check if the year directory already exists
	folder_id = ""
	query = {'q': "'" + id + "'" + " in parents and trashed=false"}
	file_list = drive.ListFile(query).GetList()
	for file_folder in file_list:
		if file_folder['title'] == str(folder_name):
			return file_folder['id']

	return None