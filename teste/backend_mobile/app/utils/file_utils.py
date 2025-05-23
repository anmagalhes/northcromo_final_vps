from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from app.config import GOOGLE_CREDENTIALS_PATH
from fastapi import UploadFile


def authenticate_google_drive():
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
    )

    service = build("drive", "v3", credentials=credentials)
    return service


def upload_file_to_drive(file: UploadFile, file_name: str):
    service = authenticate_google_drive()

    # Carregar o conteúdo do arquivo recebido pelo FastAPI (em memória)
    file_content = file.file.read()

    # Usar BytesIO para converter os dados binários em algo que o Google API pode entender
    file_stream = io.BytesIO(file_content)

    mime_type = file.content_type  # Vamos usar o tipo MIME enviado pelo FastAPI

    media = MediaIoBaseUpload(file_stream, mimetype=mime_type)

    # Realizar o upload para o Google Drive
    request = service.files().create(
        media_body=media, body={"name": file_name, "mimeType": mime_type}
    )

    # Executar o request
    uploaded_file = request.execute()
    return uploaded_file
