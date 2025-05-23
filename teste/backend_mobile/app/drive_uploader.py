from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
from app.config import GOOGLE_CREDENTIALS_PATH
from fastapi import UploadFile

# ID da pasta no Google Drive onde os arquivos serão armazenados
FOLDER_ID = "1xXBXQKFydOjsXgC3j4Sqiaya873Yx31o"


def authenticate_google_drive():
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]

    # Carrega as credenciais do arquivo JSON
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
    )

    # Constrói o serviço para a API do Google Drive
    service = build("drive", "v3", credentials=credentials)
    return service


def upload_file_to_drive(file: UploadFile, file_name: str):
    service = authenticate_google_drive()

    # Lê o conteúdo do arquivo
    file_content = file.file.read()

    # Cria um objeto de arquivo em memória (BytesIO) para ser enviado para o Google Drive
    file_stream = io.BytesIO(file_content)

    # Define o tipo MIME com base no tipo de conteúdo fornecido pelo FastAPI
    mime_type = file.content_type

    # Cria o objeto de upload
    media = MediaIoBaseUpload(file_stream, mimetype=mime_type, resumable=True)

    # Criação do arquivo no Google Drive com a pasta específica
    file_metadata = {
        "name": file_name,  # Nome do arquivo
        "parents": [FOLDER_ID],  # Pasta onde o arquivo será armazenado
    }

    try:
        # Solicita a criação do arquivo no Google Drive
        request = service.files().create(media_body=media, body=file_metadata)

        # Executa a solicitação e retorna o arquivo criado
        uploaded_file = request.execute()
        return uploaded_file

    except Exception as e:
        return {"error": str(e)}
