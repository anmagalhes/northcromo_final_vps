# app/__init__.py
from fastapi import FastAPI
from app.cliente.routes import router as cliente_router
from app.database import engine, Base

# Criar as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Criar a instância do FastAPI
app = FastAPI()

# Registrar as rotas
app.include_router(cliente_router, prefix="/api/cliente", tags=["cliente"])

# Dependência para o banco de dados (passando a sessão)
from app.database import get_db
from fastapi import Depends

@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # Exemplo simples de rota usando o banco de dados
    return {"message": "Olá, Mundo!"}
