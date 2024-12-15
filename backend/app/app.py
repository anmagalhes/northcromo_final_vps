import asyncio
from flask import Flask, jsonify
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from database import init_db  # A função assíncrona que inicializa o banco de dados
from frontend_blueprint import frontend_bp  # Importação absoluta


# Registra os blueprints
from auth import auth_blueprint
from users import users_blueprint
from defeitos import defeito_blueprint
from checklist_recebimento import checklist_recebimento_blueprint

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)

# Função para inicializar o banco de dados de forma assíncrona
async def initialize_database():
    # Inicializa o banco de dados de forma assíncrona
    engine, Session = await init_db(app)  # Chama a função que retorna o engine e a session
    
    # Inicializa o Migrate para gerenciar migrações
    migrate = Migrate(app, db)

    # Aqui você pode adicionar qualquer código adicional necessário para a configuração do banco de dados
    return engine

# Função principal de criação do app
async def create_app():
    await initialize_database()  # Inicializa o banco de dados de forma assíncrona
    
    # Registra o blueprint do frontend
    app.register_blueprint(frontend_bp)  # Registra o blueprint do frontend
    # Registra os blueprints
    app.register_blueprint(auth_blueprint, url_prefix='/auth')  # Rotas de autenticação
    app.register_blueprint(users_blueprint, url_prefix='/users')  # Rotas de usuários
    app.register_blueprint(defeito_blueprint, url_prefix='/api/defeitos')  # Rotas de defeitos
    app.register_blueprint(checklist_recebimento_blueprint, url_prefix='/checklists')

     # Exemplo de rota da API
    @app.route('/api')
    def api_home():
        return jsonify({
            "status": "API is running",
            "message": "Welcome to the API endpoint!"
        })

    return app

# Função para rodar a aplicação
def run():
    # Usamos asyncio.run para inicializar o app de forma assíncrona
    asyncio.run(start_app())  # Inicia a aplicação assíncrona

async def start_app():
    app = await create_app()  # Cria a aplicação Flask com configuração assíncrona
    app.run(debug=True, host="0.0.0.0")  # Rodando Flask de maneira síncrona, mas com setup assíncrono

if __name__ == "__main__":
    run()  # Inicia o processo de execução
