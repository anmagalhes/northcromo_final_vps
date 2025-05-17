from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import os

def get_drive_service():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/drive.file']

    # Autenticação
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sistemaNortrCromo_googleConsole.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def upload_file_to_drive(file_name: str, file_content: bytes):
    service = get_drive_service()
    file_metadata = {'name': file_name}
    media = MediaIoBaseUpload(io.BytesIO(file_content), mimetype='image/jpeg')

    uploaded_file = service.files().create(
        media_body=media,
        body=file_metadata,
        fields='id'
    ).execute()

    return uploaded_file.get('id')

def generate_file_link(file_id: str):
    service = get_drive_service()

    # Obtendo o link de visualização do arquivo
    file = service.files().get(fileId=file_id, fields='webViewLink').execute()
    return file.get('webViewLink')
