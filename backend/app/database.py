# app/database.py
from sqlalchemy import text
#from sqlalchemy import create_engine, text
#from app import db


# Função para inicializar o banco de dados com a aplicação Flask
# def init_db(app):
 #   """Inicializa o banco de dados com a aplicação Flask"""
 #   db.init_app(app)  # Apenas garante que o db esteja inicializado com a aplicação


# Função para testar a conexão com o banco de dados
def test_connection(db, app):
    try:
        with app.app_context():
            with db.engine.connect() as conn:  # Usando a engine do db
                result = conn.execute(text('SELECT 1'))  # Executando uma consulta simples
                print(f"Conexão bem-sucedida: {result.fetchone()}")  # Imprime o resultado
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        raise e
