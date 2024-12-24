# app/cliente/services.py
from sqlalchemy.orm import Session
from app.models import Cliente
from app.schemas.cliente import ClienteSchema
from app.database import get_db
from fastapi import HTTPException, Depends

# Instância do schema
cliente_schema = ClienteSchema()  # Para operações com um único cliente

# Listar todos os clientes
def list_clientes(db: Session):
    clientes = db.query(Cliente).all()  # Consulta todos os clientes
    return [cliente_schema.dump(cliente) for cliente in clientes]  # Serializa e retorna a lista de clientes

# Obter um cliente específico
def get_cliente(id: int, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()  # Encontra o cliente pelo ID
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")  # Lançando exceção caso não exista
    return cliente_schema.dump(cliente)  # Serializa e retorna o cliente

# Criar um novo cliente
def create_cliente(data: dict, db: Session):
    try:
        # Validação de dados
        if not data.get('nome_cliente') or not data.get('tipo_cliente') or not data.get('doc_cliente'):
            raise ValueError("Os campos tipo_cliente, nome_cliente e doc_cliente são obrigatórios!")

        # Criar cliente
        cliente = Cliente(**data)

        # Adicionar e persistir no banco de dados
        db.add(cliente)
        db.commit()
        db.refresh(cliente)

        return cliente_schema.dump(cliente)  # Retorna o cliente serializado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Retorna erro 400 caso falte campo
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Erro ao criar o cliente: " + str(e))

# Atualizar um cliente existente
def update_cliente(id: int, data: dict, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    # Atualiza os campos com os dados fornecidos
    for key, value in data.items():
        setattr(cliente, key, value)
    
    db.commit()
    db.refresh(cliente)
    
    return cliente_schema.dump(cliente)  # Retorna o cliente atualizado

# Excluir um cliente
def delete_cliente(id: int, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"message": "Cliente deletado com sucesso"}  # Mensagem de sucesso
