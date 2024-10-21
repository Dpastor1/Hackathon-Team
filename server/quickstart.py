from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path

# If modifying these SCOPES, delete the token.json file.
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_google_drive():
    creds = None
    # Token file stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run.
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def list_subfolders(service, parent_folder_id):
    query = f"'{parent_folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    folders = results.get('files', [])

    if not folders:
        print('No subfolders found.')
    else:
        print('Subfolders:')
        for folder in folders:
            print(f"{folder['name']} (ID: {folder['id']})")
    return folders

def list_files_in_folder(service, folder_id):
    query = f"'{folder_id}' in parents"
    results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found in folder.')
    else:
        print(f'Files in folder (ID: {folder_id}):')
        for item in items:
            print(f"{item['name']} (ID: {item['id']})")

if __name__ == '__main__':
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    parent_folder_id = '1u8ZzB1cB5ClDCD7g6sNikSLksbGr9j4f'  # Folder ID found on google drive link
    subfolders = list_subfolders(service, parent_folder_id)

    for subfolder in subfolders:
        if subfolder['name'] == 'images':
            print("Monitoring images folder...")
            list_files_in_folder(service, subfolder['id'])
        elif subfolder['name'] == 'sensor data':
            print("Monitoring sensor data folder...")
            list_files_in_folder(service, subfolder['id'])

