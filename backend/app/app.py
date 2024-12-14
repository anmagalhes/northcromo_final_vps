import asyncio
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
from models import db
from database import init_db  # A função assíncrona que inicializa o banco de dados

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
    
    # Registra os blueprints
    from auth import auth_blueprint
    from users import users_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    # A rota principal
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

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
