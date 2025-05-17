# app/api/upload.py
from fastapi import APIRouter, File, UploadFile
import os
from app.settings import Settings

router = APIRouter()

UPLOAD_FOLDER = 'uploads/'  # Pasta onde as imagens serão salvas

# Função para salvar o arquivo
async def save_uploaded_file(file: UploadFile):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return file_path

@router.post("/upload-photo/")
async def upload_photo(file: UploadFile = File(...)):
    try:
        file_path = await save_uploaded_file(file)
        return {"message": f"Foto salva com sucesso em {file_path}"}
    except Exception as e:
        return {"error": str(e)}
