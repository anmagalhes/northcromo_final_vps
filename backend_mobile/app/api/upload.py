# app/api/upload.py
from fastapi import APIRouter, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.services.google_drive import upload_file_to_drive, generate_file_link
from app.database import get_db  # Importando corretamente a função get_db
from app.models import Photo  # Model para a tabela de fotos
from app.utils import get_next_sequence
from datetime import datetime

router = APIRouter()

@router.post("/upload-photo/")
async def upload_photo(
    file: UploadFile = File(...),  # Arquivo da foto
    order_id: str = "",  # ID da ordem que vem do frontend
    db: Session = Depends(get_db),  # Conexão com o banco de dados usando a função get_db
):
    try:
        # Verifica se o ID da ordem foi fornecido
        if not order_id:
            return JSONResponse(
                content={"error": "O ID da ordem é necessário para o upload."},
                status_code=400
            )

        # Ano atual, baseado no sistema
        year = datetime.now().year

        # Obtém a próxima sequência para a ordem, limitado a 5
        sequence = get_next_sequence(order_id)

        # Lê o conteúdo do arquivo enviado
        file_content = await file.read()

        # Faz o upload do arquivo para o Google Drive e obtém o ID do arquivo
        file_id = upload_file_to_drive(file.filename, file_content)

        # Gerar o link do arquivo
        file_link = generate_file_link(file_id)

        # Salva os detalhes da foto no banco de dados
        new_photo = Photo(
            order_id=order_id,
            sequence=sequence,
            year=year,
            file_name=file.filename,
            file_id=file_id,
            file_link=file_link
        )

        # Adiciona e faz commit no banco de dados
        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)

        # Retorna o link da foto
        return JSONResponse(
            content={
                "message": "Foto carregada com sucesso!",
                "file_link": file_link  # Retorna o link gerado do arquivo no Google Drive
            },
            status_code=200
        )

    except Exception as e:
        return JSONResponse(
            content={"error": f"Erro ao carregar foto: {str(e)}"},
            status_code=500
        )
