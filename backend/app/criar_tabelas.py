import sys
import os
from dotenv import load_dotenv

# Ajusta o caminho para garantir que o diretório 'app' seja tratado como pacote
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.database import db, init_db

# Função para verificar se a tabela já existe
def tabela_existe(nome_tabela):
    return db.engine.dialect.has_table(db.session.bind, nome_tabela)

# Função para criar as tabelas
def criar_tabelas():
    with create_app().app_context():  # Garante o contexto do Flask
        if os.environ.get('FLASK_ENV') == 'production':
            print("Criando tabelas no banco de produção...")
            db.create_all()
        else:
            print("Ambiente de desenvolvimento detectado. Utilizando SQLite para criação de tabelas.")
            db.create_all()

        print("Tabelas verificadas/criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()

