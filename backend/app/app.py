import asyncio
from flask import Flask
from flask_migrate import Migrate
from database import init_db  # A função assíncrona que inicializa o banco de dados
from models import db
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)


# Função principal para inicializar o banco de dados de forma assíncrona
async def create_app():
    # Inicializa o banco de dados de forma assíncrona
    engine, Session = await init_db(app)  # Chama a função que retorna o engine e o session
    
    # Inicializa Migrate para gerenciar migrations
    migrate = Migrate(app, db)

    # Registra blueprints
    from auth import auth_blueprint
    from users import users_blueprint
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(users_blueprint, url_prefix='/users')

    return app

# Ponto de entrada para rodar o app
if __name__ == "__main__":

    # Aqui usamos o asyncio.run para rodar a aplicação de forma assíncrona
    asyncio.run(create_app())  # Usando asyncio.run para rodar a aplicação de forma assíncrona
    app.run(debug=True, host="0.0.0.0")  # Roda o servidor Flask de forma síncrona
