import sys
import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from app.models.db import db
from app.database import init_db
from app.frontend_blueprint import frontend_bp

# Registra os blueprints
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.defeitos import defeito_blueprint
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
CORS(app)

# Inicializa o banco de dados (sincrono)
def initialize_database():
    # Inicializa o banco de dados
    engine, Session = init_db(app)  # Chama a função que retorna o engine e a session
    
    # Inicializa o Migrate para gerenciar migrações
    migrate = Migrate(app, db)

    return engine

# Função principal de criação do app
def create_app():
    # Inicializa o banco de dados de forma síncrona
    initialize_database()  
    
    # Registra o blueprint do frontend
    app.register_blueprint(frontend_bp)  
    
    # Registra os blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')  
    app.register_blueprint(users_blueprint, url_prefix='/api/users')  
    app.register_blueprint(defeito_blueprint, url_prefix='/api/defeitos')  
    app.register_blueprint(checklist_recebimento_blueprint, url_prefix='/api/checklist')
    app.register_blueprint(foto_recebimento_blueprint, url_prefix='/api/foto_recebimento')
    app.register_blueprint(funcionario_blueprint, url_prefix='/api/funcionario')
    app.register_blueprint(cliente_blueprint, url_prefix='/api/clientes')
    app.register_blueprint(componente_blueprint, url_prefix='/api/componente')
    
    # Exemplo de rota da API
    @app.route('/api')
    def api_home():
        return jsonify({
            "status": "API is running",
            "message": "Welcome to the API endpoint!"
        })
    
    # Tratamento de erro global
    @app.errorhandler(Exception)
    def handle_error(e):
        # Loga o erro (pode ser ajustado para salvar os logs em um arquivo ou sistema de logs)
        print(f"Error: {str(e)}")
        
        # Retorna uma resposta amigável ao usuário
        return jsonify({
            "status": "error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500  # Retorna código de erro 500 (erro interno do servidor)

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


# Função principal para rodar a aplicação (não usar app.run() aqui)
def run():
    app = create_app()
    return app

if __name__ == "__main__":
    # NÃO use app.run() em produção! Use Gunicorn ou outro servidor WSGI.
    app = create_app()


