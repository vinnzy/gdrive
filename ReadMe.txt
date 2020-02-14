Read and Follow this instruction before you execute the code

1. Go to APIs Console and make your own project.
2. Search for ‘Google Drive API’, select the entry, and click ‘Enable’.
3. Select ‘Credentials’ from the left menu, click ‘Create Credentials’, select ‘OAuth client ID’.
4. Now, the product name and consent screen need to be set -> click ‘Configure consent screen’ and follow the instructions. Once finished:
   1. Select ‘Application type’ to be Web application.
   2. Enter an appropriate name.
   3. Input http://localhost:8080 for ‘Authorized JavaScript origins’.
   4. Input http://localhost:8080/ for ‘Authorized redirect URIs’.
   5. Click ‘Save’.

Click ‘Download JSON’ on the right side of Client ID to download client_secret_<really long ID>.json. Rename it to client_secrets.json and save it in the working directory
The downloaded file has all authentication information of your application.

5. Update settings.yaml
    1. client_id: Get you ID from the downloaded file and update it in this file
    2. client_secret: Get your secret from the downloaded file and update here

6. Run install.sh to install the dependencies
7. The first time you execute, you have to authorize. Once its done, a creds.txt will be created and used for further authorizations


TO UPLOAD FILES IN A FOLDER
python3 main.py -u source_directory_path
Ex: python3 main.py -u /home/user/folder

