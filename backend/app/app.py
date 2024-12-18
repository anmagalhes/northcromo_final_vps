import sys
import os

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models import some_function
from app.models.db import db
from app.database import init_db  # A função assíncrona que inicializa o banco de dados
from app.frontend_blueprint import frontend_bp  # Importação absoluta

# Registra os blueprints
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.defeitos import defeito_blueprint
from app.checklist_recebimento import checklist_recebimento_blueprint
from app.foto_recebimento import foto_recebimento_blueprint
from app.funcionario import funcionario_blueprint
from app.cliente import cliente_blueprint
from app.componente import componente_blueprint
#from grupo_produto  import grupo_produto_blueprint

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)
CORS(app)

# Função para inicializar o banco de dados de forma assíncrona
async def initialize_database():
    # Inicializa o banco de dados de forma assíncrona
    engine, Session = await init_db(app)  # Chama a função que retorna o engine e a session
    
    # Inicializa o Migrate para gerenciar migrações
    migrate = Migrate(app, db)

    # Aqui você pode adicionar qualquer código adicional necessário para a configuração do banco de dados
    return engine

# Função principal de criação do app
def create_app():
    # Criação do app Flask
    app = Flask(__name__)
    CORS(app)
    
    # Registra os blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(users_blueprint, url_prefix='/api/users')
    app.register_blueprint(defeito_blueprint, url_prefix='/api/defeitos')
    app.register_blueprint(checklist_recebimento_blueprint, url_prefix='/api/checklist')
    app.register_blueprint(foto_recebimento_blueprint, url_prefix='/api/foto_recebimento')
    app.register_blueprint(funcionario_blueprint, url_prefix='/api/funcionario')
    app.register_blueprint(cliente_blueprint, url_prefix='/api/clientes')
    app.register_blueprint(componente_blueprint, url_prefix='/api/componente')
    
    @app.route('/api')
    def api_home():
        return jsonify({
            "status": "API is running",
            "message": "Welcome to the API endpoint!"
        })
    
    @app.errorhandler(Exception)
    def handle_error(e):
        print(f"Error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500
    
    return app

# Funções para abrir e fechar a sessão do banco de dados para cada requisição
@app.before_request
def before_request():
    """Abre a sessão do banco de dados antes de cada requisição"""
    g.db_session = db.session()

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

# Função principal para rodar a aplicação em produção com Gunicorn
if __name__ == "__main__":
    from gunicorn.app.base import BaseApplication

    class GunicornApp(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load(self):
            return self.application

        def load_config(self):
            config = {
                'bind': '0.0.0.0:5000',
                'workers': 4,  # Ajuste o número de workers conforme necessário
                'worker_class': 'gevent',  # Usando worker assíncrono gevent
                'loglevel': 'info',  # Defina o nível de log
            }
            for key, value in config.items():
                self.cfg.set(key, value)

    # Inicializa o banco de dados de forma assíncrona
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_database())  # Inicia o banco de dados

    # Criação do app Flask
    app = create_app()

    # Inicializa o Gunicorn
    gunicorn_app = GunicornApp(app)
    gunicorn_app.run()
