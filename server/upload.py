import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from googleapiclient.http import MediaFileUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

def auth():
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
                    'credentials1.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)
        return service
# 1hIlXQq4U62mSKnnllXeerWlSNmHdoeWW
def get_or_create_folder(service, folder_name):
    parent = '1hIlXQq4U62mSKnnllXeerWlSNmHdoeWW'
    # Check if the folder already exists in Google Drive
    folder_query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and '{parent}' in parents"
    folders = service.files().list(q=folder_query, spaces='drive', fields='files(id)').execute().get('files', [])

    if folders:
        # Folder already exists, return the folder ID
        return folders[0]['id']
    else:
        # Folder does not exist, create a new one and return the folder ID
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [parent]
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        return folder.get('id')

def uploadfile(file):
    data = file.split['/']
    service = auth()
    folder_id = get_or_create_folder(service,data[0])

    # Upload the PDF file to the folder
    name = data[1]+data[2]
    file_metadata = {
        'name': os.path.basename(name),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file, mimetype='application/pdf')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()


    print(f"PDF file uploaded successfully with ID: {file.get('id')}")

uploadfile('DEC test.pdf')    