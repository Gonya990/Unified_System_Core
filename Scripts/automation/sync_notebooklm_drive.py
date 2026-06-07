import io
import logging
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('DriveSync')

# Scopes for Google Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Paths
BASE_DIR = Path('/Users/igorgoncharenko/Documents/Unified_System_Core')
CREDENTIALS_DIR = BASE_DIR / 'Scripts' / 'automation' / '.credentials'
CLIENT_SECRET_FILE = CREDENTIALS_DIR / 'gmail_credentials.json'
TOKEN_FILE = CREDENTIALS_DIR / 'drive_token.json'
INBOX_DIR = BASE_DIR / 'Agent_Context' / 'Knowledge_Base' / 'notebooklm' / '_inbox'

def authenticate():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET_FILE.exists():
                logger.error(f"Client secret file not found: {CLIENT_SECRET_FILE}")
                logger.error("Please ensure you have downloaded your OAuth client secrets from Google Cloud Console.")
                exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

def sync_notebooklm_folder(service, folder_name="NotebookLM"):
    # Find the folder
    results = service.files().list(
        q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false",
        spaces='drive',
        fields='nextPageToken, files(id, name)'
    ).execute()

    items = results.get('files', [])

    if not items:
        logger.warning(f"No folder found named '{folder_name}'.")
        return

    folder_id = items[0]['id']
    logger.info(f"Found folder: {folder_name} (ID: {folder_id})")

    # Ensure inbox directory exists
    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    # List files in the folder
    page_token = None
    while True:
        response = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType)',
            pageToken=page_token
        ).execute()

        for file in response.get('files', []):
            file_id = file.get('id')
            file_name = file.get('name')
            mime_type = file.get('mimeType')

            target_path = INBOX_DIR / file_name

            # If it's a Google Doc, we export it. Otherwise, we download it.
            if mime_type.startswith('application/vnd.google-apps.'):
                if mime_type == 'application/vnd.google-apps.document':
                    target_path = target_path.with_suffix('.txt')
                    if target_path.exists():
                        continue # skip already downloaded

                    logger.info(f"Exporting Google Doc: {file_name} -> {target_path.name}")
                    request = service.files().export_media(fileId=file_id, mimeType='text/plain')
                else:
                    logger.info(f"Skipping unsupported Google App file: {file_name} ({mime_type})")
                    continue
            else:
                if target_path.exists():
                    continue # skip already downloaded

                logger.info(f"Downloading file: {file_name}")
                request = service.files().get_media(fileId=file_id)

            try:
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()

                with open(target_path, 'wb') as f:
                    f.write(fh.getvalue())
            except Exception as e:
                logger.error(f"Failed to download {file_name}: {e}")

        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break

if __name__ == '__main__':
    logger.info("Starting NotebookLM Google Drive Sync...")
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    sync_notebooklm_folder(service)
    logger.info("Sync complete.")
