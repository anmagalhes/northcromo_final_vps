# app.py
import sys
import os
from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from dotenv import load_dotenv
from app import db  # Função para inicializar o banco de dados

# Registra os blueprints
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.defeito import defeito_blueprint
from app.checklist_recebimento import checklist_recebimento_blueprint
from app.foto_recebimento import foto_recebimento_blueprint
from app.funcionario import funcionario_blueprint
from app.cliente import cliente_blueprint
from app.componente import componente_blueprint

# Carregar as variáveis do arquivo .env
load_dotenv()

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Inicializa o Flask app
app = Flask(__name__)


# Configurações
app.config.from_object(Config)  # Usa a configuração do arquivo .env ou settings


# Função para inicializar o banco de dados
def initialize_database(app):
    # Seleciona a configuração dependendo do ambiente (Desenvolvimento ou Produção)
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object('app.config.ProductionConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    # Agora que as configurações estão carregadas, inicialize o banco de dados
    db.init_app(app)  # Inicializa o SQLAlchemy com a app
    migrate = Migrate(app, db)  # Inicializa o Migrate para gerenciar migrações

# Função principal de criação do app
def create_app():
    initialize_database(app)  # Inicializa o banco de dados de forma síncrona
    
    # Registra os blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')  # Rotas de autenticação
    app.register_blueprint(users_blueprint, url_prefix='/api/users')  # Rotas de usuários
    app.register_blueprint(defeito_blueprint, url_prefix='/api/defeitos')  # Rotas de defeitos
    app.register_blueprint(checklist_recebimento_blueprint, url_prefix='/api/checklist')
    app.register_blueprint(foto_recebimento_blueprint, url_prefix='/api/foto_recebimento')
    app.register_blueprint(funcionario_blueprint, url_prefix='/api/funcionario')
    app.register_blueprint(cliente_blueprint, url_prefix='/api/cliente')
    app.register_blueprint(componente_blueprint, url_prefix='/api/componente')

    # Exemplo de rota da API
    @app.route('/api')
    def api_home():
        return jsonify({
            "status": "API is running",
            "message": "Welcome to the API endpoint!"
        })

    return app

# Funções para abrir e fechar a sessão do banco de dados para cada requisição
@app.before_request
def before_request():
    """Abre a sessão do banco de dados antes de cada requisição"""
    g.db_session = db.session()  # Usando o sessionmaker para abrir a conexão

@app.after_request
def after_request(response):
    """Fecha a sessão do banco de dados após a requisição"""
    try:
        g.db_session.commit()  # Commitando a transação (se necessário)
    except Exception as e:
        g.db_session.rollback()  # Em caso de erro, faz rollback
    finally:
        g.db_session.close()  # Fecha a sessão do banco de dados
    return response

for rule in app.url_map.iter_rules():
    print(rule)
    
# Definindo a variável 'application' que o Gunicorn precisa para rodar a aplicação
application = create_app()  # Gunicorn vai procurar por 'application'



# Se desejar rodar localmente com Flask (não no Gunicorn), você pode descomentar as linhas abaixo
#if __name__ == "__main__":
 #   create_app()  # Cria o app
  #  app.run()  # Rodando o Flask de forma síncrona