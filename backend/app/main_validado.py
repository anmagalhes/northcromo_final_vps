# main.py
import sys
import os
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from config import Config, ProductionConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.user import users_router  # Importando o router de usuários
#from app.defeito import defeito_router  # Importando o router de defeitos
#from app.checklist_recebimento import checklist_recebimento_router  # Ajuste nos imports
#from app.foto_recebimento import foto_router
#from app.funcionario import  funcionario_router
from app.cliente import cliente_router
#from app.componente import componente_router


# Carregar as variáveis do arquivo .env
load_dotenv()

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Ajustando para usar a variável de ambiente ou a configuração correta
config = DevelopmentConfig if os.getenv("ENV") == "development" else ProductionConfig
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", config.SQLALCHEMY_DATABASE_URI)

# Criação do engine e da sessão do SQLAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Inicializa o FastAPI
app = FastAPI()

# Registra os routers (não blueprints no FastAPI)
app.include_router(users_router, prefix='/api/users', tags=["users"])
#app.include_router(defeito_router, prefix='/api/defeitos', tags=["defeitos"])
#app.include_router(checklist_recebimento_router, prefix='/api/checklist', tags=["checklist"])
#app.include_router(foto_router, prefix='/api/foto_recebimento', tags=["foto_recebimento"])
#app.include_router(funcionario_router, prefix='/api/funcionario', tags=["funcionario"])
app.include_router(cliente_router, prefix='/api/cliente', tags=["cliente"])
#app.include_router(componente_router, prefix='/api/componente', tags=["componente"])

@app.get("/api")
async def api_home():
    return JSONResponse({
        "status": "API is running",
        "message": "Welcome to the API endpoint!"
    })

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Variável 'application' que o Gunicorn espera (opcional, apenas para Gunicorn)
application = app
