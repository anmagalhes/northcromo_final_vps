import sys
import os

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, g
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models import some_function
from app.models.db import db
from app.database import init_db  # A função para inicializar o banco de dados
from app.frontend_blueprint import frontend_bp  # Importação do blueprint do frontend

# Registra os blueprints
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.defeitos import defeito_blueprint
from app.checklist_recebimento import checklist_recebimento_blueprint
from app.foto_recebimento import foto_recebimento_blueprint
from app.funcionario import funcionario_blueprint
from app.cliente import cliente_blueprint
from app.componente import componente_blueprint
#from grupo_produto import grupo_produto_blueprint

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)


# Função para inicializar o banco de dados
def initialize_database():
    # Inicializa o banco de dados de forma síncrona
    engine, Session = init_db(app)  # Chama a função que retorna o engine e a session
    
    # Inicializa o Migrate para gerenciar migrações
    migrate = Migrate(app, db)

    # Aqui você pode adicionar qualquer código adicional necessário para a configuração do banco de dados
    return engine

# Função principal de criação do app
def create_app():
    initialize_database()  # Inicializa o banco de dados de forma síncrona
    
    # Registra o blueprint do frontend
    app.register_blueprint(frontend_bp)  # Registra o blueprint do frontend
    # Registra os blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')  # Rotas de autenticação
    app.register_blueprint(users_blueprint, url_prefix='/api/users')  # Rotas de usuários
    app.register_blueprint(defeito_blueprint, url_prefix='/api/defeitos')  # Rotas de defeitos
    app.register_blueprint(checklist_recebimento_blueprint, url_prefix='/api/checklist')
    app.register_blueprint(foto_recebimento_blueprint, url_prefix='/api/foto_recebimento')
    app.register_blueprint(funcionario_blueprint, url_prefix='/api/funcionario')
    app.register_blueprint(cliente_blueprint, url_prefix='/api/cliente')
    app.register_blueprint(componente_blueprint, url_prefix='/api/componente')
    #app.register_blueprint(grupo_produto_blueprint, url_prefix='/grupo_produto')

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

# Definindo a variável 'application' que o Gunicorn precisa para rodar a aplicação
application = create_app()  # Gunicorn vai procurar por 'application'

# DEV
# Função para rodar a aplicação
#if __name__ == "__main__":
#    create_app()  # Cria o app
#    app.run()  # Rodando o Flask de forma síncrona
