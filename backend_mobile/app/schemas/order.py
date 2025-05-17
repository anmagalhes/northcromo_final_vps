# app/api/order.py

from fastapi import APIRouter, HTTPException, Depends, File, UploadFile
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Order, Photo  # Importa os modelos de Ordem e Foto
import uuid  # Para gerar um ID único para a ordem
from app.google_drive import upload_file_to_drive, generate_file_link
from app.utils import get_next_sequence
from datetime import datetime

router = APIRouter()

# Dependência para obter a sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint para criar a ordem
@router.post("/create-order/")
async def create_order(description: str, db: Session = Depends(get_db)):
    try:
        order_id = str(uuid.uuid4())  # Gerar um ID único para a ordem
        new_order = Order(id=order_id, description=description)

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return {"order_id": new_order.id, "description": new_order.description}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar ordem: {str(e)}")

# Endpoint para editar a ordem
@router.put("/edit-order/{order_id}/")
async def edit_order(order_id: str, description: str, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")

        order.description = description

        db.commit()
        db.refresh(order)

        return {"order_id": order.id, "description": order.description}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao editar ordem: {str(e)}")

# Endpoint para excluir a ordem
@router.delete("/delete-order/{order_id}/")
async def delete_order(order_id: str, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")

        db.delete(order)
        db.commit()

        return {"message": "Ordem excluída com sucesso"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao excluir ordem: {str(e)}")

# Endpoint para exibir a ordem
@router.get("/get-order/{order_id}/")
async def get_order(order_id: str, db: Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        if not order:
            raise HTTPException(status_code=404, detail="Ordem não encontrada")

        photos = db.query(Photo).filter(Photo.order_id == order_id).all()

        photos_data = [{"file_name": photo.file_name, "file_link": photo.file_link} for photo in photos]

        return {
            "order_id": order.id,
            "description": order.description,
            "photos": photos_data
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao exibir ordem: {str(e)}")

# Endpoint para upload de fotos
@router.post("/upload-photo/")
async def upload_photo(
    file: UploadFile = File(...),
    order_id: str = "",
    db: Session = Depends(get_db),
):
    try:
        if not order_id:
            raise HTTPException(status_code=400, detail="O ID da ordem é necessário para o upload.")

        file_content = await file.read()

        file_id = upload_file_to_drive(file.filename, file_content)

        file_link = generate_file_link(file_id)

        new_photo = Photo(
            order_id=order_id,
            file_name=file.filename,
            file_id=file_id,
            file_link=file_link,
            sequence=get_next_sequence(order_id),
            year=datetime.now().year
        )

        db.add(new_photo)
        db.commit()
        db.refresh(new_photo)

        return {"message": "Foto carregada com sucesso!", "file_link": file_link}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao carregar foto: {str(e)}")
