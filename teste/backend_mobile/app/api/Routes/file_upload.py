import os
import io
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from typing import List

router = APIRouter()

SERVICE_ACCOUNT_FILE = "sistemaNortrCromo_googleConsole.json"
SCOPES = ["https://www.googleapis.com/auth/drive.file"]  # Permissão para upload de arquivos
FOLDER_ID = "1xXBXQKFydOjsXgC3j4Sqiaya873Yx31o"  # Substitua pelo ID da sua pasta no Google Drive

# Função para autenticar com a conta de serviço
def authenticate_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("drive", "v3", credentials=credentials)

# Função para verificar ou criar pasta no Google Drive
def get_or_create_folder(service, folder_name: str, parent_folder_id: str) -> str:
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}' and '{parent_folder_id}' in parents"
    results = service.files().list(q=query, spaces="drive", fields="files(id, name)").execute()
    folders = results.get("files", [])

    if folders:
        return folders[0]["id"]

    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_folder_id]
    }
    folder = service.files().create(body=folder_metadata, fields="id").execute()
    return folder["id"]

# Função para enviar o arquivo para o Google Drive
def upload_to_drive(file_name: str, file_bytes: bytes, mime_type: str, cliente: str):
    service = authenticate_service()

    pasta_cliente_id = get_or_create_folder(service, cliente, FOLDER_ID)

    file_metadata = {
        "name": file_name,
        "parents": [pasta_cliente_id]
    }

    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mime_type)

    try:
        file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
        file_id = file.get("id")

        # Define permissão pública
        service.permissions().create(
            fileId=file_id,
            body={"type": "anyone", "role": "reader"}
        ).execute()

        file = service.files().get(fileId=file_id, fields="webViewLink").execute()
        return file.get("webViewLink")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload: {str(e)}")

# Endpoint para fazer upload de múltiplas fotos
@router.post("/adicionarOrdem")
async def adicionar_ordem(
    fotos: List[UploadFile] = File(...),
    cliente: str = Form(...),
):
    file_links = []  # Lista para armazenar os links dos arquivos enviados

    for foto in fotos:
        file_content = await foto.read()
        mime_type = foto.content_type

        try:
            file_link = upload_to_drive(foto.filename, file_content, mime_type, cliente)
            file_links.append(file_link)  # Adiciona o link à lista
        except HTTPException as e:
            return {"error": str(e.detail)}

    return {"file_links": file_links}
