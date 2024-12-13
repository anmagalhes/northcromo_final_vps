from flask import Flask
from flask_migrate import Migrate
from database import init_db
from models import db
from dotenv import load_dotenv

# Carregar as variáveis do arquivo .env
load_dotenv()

# Inicializa o Flask app
app = Flask(__name__)

# Inicializa o banco de dados
engine, Session = init_db(app)  # Chama a função que retorna o engine e o session

# Inicializa Migrate para gerenciar migrations
migrate = Migrate(app, db)

# Registra blueprints
from auth import auth_blueprint
from users import users_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(users_blueprint, url_prefix='/users')

# Ponto de entrada
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
