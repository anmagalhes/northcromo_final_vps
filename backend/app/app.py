# app.py
import sys
import os

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, g
from flask_migrate import Migrate
from dotenv import load_dotenv
#from app.models import some_function
from app.database import db, init_db  # Agora importa o 'db' diretamente

# Registra os blueprints
from app.frontend_blueprint import frontend_bp  # Importação do blueprint do frontend
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.checklist_recebimento import checklist_recebimento_blueprint
from app.foto_recebimento import foto_recebimento_blueprint
from app.funcionario import funcionario_blueprint
from app.cliente import cliente_blueprint
from app.componente import componente_blueprint

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)
app.config['ENV'] = 'development'

# Função para inicializar o banco de dados
def initialize_database():
    # Inicializa o banco de dados diretamente com o SQLAlchemy
    init_db(app)  # Chama a função que inicializa o banco de dados
    migrate = Migrate(app, db)  # Inicializa o Migrate para gerenciar migrações
    return app

# Função principal de criação do app
def create_app():
    app = initialize_database()  # Inicializa o banco de dados de forma síncrona
    
    # Registra os blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(users_blueprint, url_prefix='/api/users')
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
    g.db_session = db.session  # Usa a sessão do db diretamente

@app.after_request
def after_request(response):
    """Fecha a sessão do banco de dados após a requisição"""
    try:
        g.db_session.commit()  # Commitando a transação (se necessário)
    except Exception as e:
        g.db_session.rollback()  # Em caso de erro, faz rollback
    finally:
        g.db_session.remove()  # Fecha a sessão do banco de dados
    return response

# Definindo a variável 'application' que o Gunicorn precisa para rodar a aplicação
application = create_app()  # Gunicorn vai procurar por 'application'

# DEV teste
# Função para rodar a aplicação
#if __name__ == "__main__":
 #   create_app()  # Cria o app
 #   app.run(debug=True)  # Rodando o Flask de forma síncrona