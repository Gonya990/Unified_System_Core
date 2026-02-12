import io
import pickle
from pathlib import Path

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']

LOCAL_CONTEXT_DIR = Path("/Users/igorgoncharenko/Documents/Unified_System_Core/Context")
CREDENTIALS_FILE = Path(__file__).resolve().parent.parent.parent.parent.parent / "Projects/AI_Core/config/gmail_credentials.json"
TOKEN_FILE = Path(__file__).parent / "drive_token.pickle"

def get_drive_service():
    creds = None
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_FILE.exists():
                print(f"❌ Credentials file not found at {CREDENTIALS_FILE}")
                return None
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)

def list_files(service, folder_id=None):
    results = service.files().list(
        pageSize=100,
        fields="nextPageToken, files(id, name, mimeType)",
        q=f"'{folder_id}' in parents" if folder_id else "name = 'Context' and mimeType = 'application/vnd.google-apps.folder'"
    ).execute()
    return results.get('files', [])

def create_folder(service, name, parent_id=None):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]

    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def sync_context_folder():
    service = get_drive_service()
    if not service:
        return

    print("🔄 Checking Google Drive connection...")

    # 1. Find or Create 'Context' folder on Drive
    results = list_files(service)
    if not results:
        print("📁 'Context' folder not found on Drive. Creating...")
        folder_id = create_folder(service, "Context")
    else:
        folder_id = results[0]['id']
        print(f"📁 Found 'Context' folder: {folder_id}")

    # 2. Upload missing local files
    print("📤 Syncing Local -> Drive...")
    if not LOCAL_CONTEXT_DIR.exists():
        LOCAL_CONTEXT_DIR.mkdir(parents=True)

    drive_files = list_files(service, folder_id)
    drive_filenames = [f['name'] for f in drive_files]

    for file_path in LOCAL_CONTEXT_DIR.glob("*"):
        if file_path.name not in drive_filenames and file_path.is_file():
            print(f"⬆️ Uploading {file_path.name}...")
            file_metadata = {'name': file_path.name, 'parents': [folder_id]}
            media = MediaFileUpload(str(file_path), resumable=True)
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # 3. Download missing Drive files
    print("📥 Syncing Drive -> Local...")
    for file in drive_files:
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            continue

        local_file = LOCAL_CONTEXT_DIR / file['name']
        if not local_file.exists():
            print(f"⬇️ Downloading {file['name']}...")
            request = service.files().get_media(fileId=file['id'])
            fh = io.FileIO(local_file, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                # print(f"Download {int(status.progress() * 100)}%.")

    print("✅ Sync Complete!")

if __name__ == '__main__':
    sync_context_folder()
