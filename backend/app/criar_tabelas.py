# app/criar_tabelas.py
from flask_migrate import Migrate  # Importando a classe Migrate corretamente
from app import create_app, db  # Importa a função create_app e o banco de dados
from app.models import (User)  # Inclua os modelos desejados

def criar_tabelas():
    app = create_app()  # Cria a instância do Flask
    migrate = Migrate(app, db)  # Agora você pode usar a instância 'migrate'
    with app.app_context():  # Cria o contexto da aplicação para que o db.create_all() funcione
        print("Conectando ao banco de dados:", app.config['SQLALCHEMY_DATABASE_URI'])
        
        # Criação das tabelas
        db.create_all()  # Cria todas as tabelas definidas nos modelos importados
        print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()  # Chama a função para criar as tabelas
