# app.py
import sys
import os

# Ajuste do Python Path para garantir que o diretório correto seja encontrado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Debug: Verificar o sys.path
print(sys.path)

from flask import Flask, jsonify, g
from database import db, init_db  # Importando 'db' e 'init_db' de 'database.py'
from app.models import some_function  # Exemplo de importação de modelo
from app.frontend_blueprint import frontend_bp  # Importação do blueprint do frontend

# Registra os blueprints
from app.auth import auth_blueprint
from app.user import users_blueprint
from app.checklist_recebimento import checklist_recebimento_blueprint
from app.foto_recebimento import foto_recebimento_blueprint
from app.funcionario import funcionario_blueprint
from app.cliente import cliente_blueprint
from app.componente import componente_blueprint

# Carregar as variáveis do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)

# Função principal de criação do app
def create_app():
    init_db(app)  # Inicializa o banco de dados com a aplicação

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

# Definindo a variável 'application' que o Gunicorn precisa para rodar a aplicação
application = create_app()

# Dev: Rodar a aplicação em modo debug
if __name__ == "__main__":
    application.run(debug=True)
