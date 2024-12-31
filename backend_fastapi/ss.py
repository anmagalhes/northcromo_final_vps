# app/criar_tabelas.py ou app/main.py (ou qualquer script de sua escolha)
from sqlalchemy.orm import Session
from app.core.config import SessionLocal  # importando a sessão
from app.models.user import User  # Importando o modelo User

# Função para buscar todos os usuários
def get_all_users(db: Session):
    return db.query(User).all()  # Retorna todos os registros da tabela 'usuario'

# Função para inicializar a sessão e rodar a consulta
def fetch_users():
    db = SessionLocal()  # Cria uma sessão com o banco
    try:
        users = get_all_users(db)  # Chama a função para buscar os dados
        for user in users:
            print(user)  # Aqui você pode personalizar para mostrar como preferir
    finally:
        db.close()  # Fecha a sessão

# Chame a função para executar
if __name__ == "__main__":
    fetch_users()
