from flask import Flask
from flask_migrate import Migrate
from auth import auth_blueprint
from users import users_blueprint
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Inicializa o Flask app
app = Flask(__name__)
# Verifica o ambiente e configura a URI do banco de dados
if os.environ.get('FLASK_ENV') == 'production':
    # Para produção com PostgreSQL
    DATABASE_URI = 'postgresql+psycopg2://flask_user:tonyteste@147.93.12.171:5432/northcromo'
else:
    # Para desenvolvimento com SQLite
    DATABASE_URI = 'sqlite:///northcromo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar tracking de modificações

# Criar o engine diretamente com SQLAlchemy
engine = create_engine(DATABASE_URI)

# Criar a fábrica de sessões manualmente (sessionmaker)
Session = sessionmaker(bind=engine)
session = Session()

# Inicializa Migrate para gerenciar migrations (opcional, caso queira usar)
migrate = Migrate(app, engine)

# Testa a conexão com o banco de dados
try:
    with engine.connect() as conn:
        # Executa a query de teste
        conn.execute(text('SELECT 1'))
    print("Conexão com o banco de dados bem-sucedida!")
except Exception as e:
    print(f"Erro ao conectar com o banco de dados: {e}")

# Registra blueprints
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(users_blueprint, url_prefix='/users')

# Ponto de entrada
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")