import asyncio
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.http import MediaIoBaseUpload
import io
import time

from app.config import GOOGLE_CREDENTIALS_PATH

# IDs
DOC_TEMPLATE_ID = "1VIrF8PyUYe-DCIeDBv3Nmiy8if7pIPhl9zA7jM50PhE"
FOLDER_ID_DESTINO = "1fstEX_fgNPnzBEeu1szOvZ43AdMTPTjk"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/documents"
]

import json


def build_services():
    credentials = service_account.Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS_PATH, scopes=SCOPES
    )
    drive_service = build("drive", "v3", credentials=credentials)
    docs_service = build("docs", "v1", credentials=credentials)
    return drive_service, docs_service

async def gerar_pdf_async(id_recebimento: int, dados: dict):
    return await asyncio.to_thread(gerar_pdf_dinamico, id_recebimento, dados)


def gerar_pdf_dinamico(id_recebimento: int, dados: dict):

    with open(GOOGLE_CREDENTIALS_PATH) as f:
        creds_json = json.load(f)
        print("📢 Conta de serviço em uso:", creds_json.get("client_email"))

    drive_service, docs_service = build_services()

    nome_arquivo = f"NothCromo_ChecklistRecebimento_{id_recebimento}"

    # 1. Buscar e deletar arquivos existentes com mesmo nome na pasta destino
    query = f"name = '{nome_arquivo}' and '{FOLDER_ID_DESTINO}' in parents and trashed = false"
    resultados = drive_service.files().list(q=query, fields="files(id, name)").execute()
    arquivos_existentes = resultados.get("files", [])

    for arquivo in arquivos_existentes:
        drive_service.files().delete(fileId=arquivo["id"]).execute()

    # 2. Copiar o template
    copied_file = drive_service.files().copy(
        fileId=DOC_TEMPLATE_ID,
        body={"name": nome_arquivo, "parents": [FOLDER_ID_DESTINO]}
    ).execute()

    copy_id = copied_file["id"]

    # 3. Preencher placeholders no documento copiado
    requests = []
    for chave, valor in dados.items():
        requests.append({
            "replaceAllText": {
                "containsText": {"text": f"{{{{{chave}}}}}", "matchCase": True},
                "replaceText": str(valor)
            }
        })

    docs_service.documents().batchUpdate(
        documentId=copy_id,
        body={"requests": requests}
    ).execute()

    time.sleep(2)  # Aguarda salvar

    # 4. Exportar para PDF
    pdf_data = drive_service.files().export(
        fileId=copy_id,
        mimeType="application/pdf"
    ).execute()

    media = io.BytesIO(pdf_data)

    # 5. Criar o arquivo PDF na pasta destino
    pdf_file = drive_service.files().create(
        body={
            "name": f"{nome_arquivo}.pdf",
            "parents": [FOLDER_ID_DESTINO],
            "mimeType": "application/pdf"
        },
        media_body=MediaIoBaseUpload(media, mimetype="application/pdf", resumable=False),
        fields="id, webViewLink"
    ).execute()

    # 6. Deletar o documento copiado do Google Docs, pois não é mais necessário
    drive_service.files().delete(fileId=copy_id).execute()

    return {"pdf_url": pdf_file["webViewLink"]}
