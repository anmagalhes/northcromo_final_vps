from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os
from models import db

# Inicializa o Flask app
app = Flask(__name__)

# Variáveis de configuração para o banco de dados
if os.environ.get('FLASK_ENV') == 'production':
    # Para produção com PostgreSQL
    DATABASE_URI = 'postgresql+psycopg2://flask_user:tonyteste@147.93.12.171:5432/northcromo'
else:
    # Para desenvolvimento com SQLite
    DATABASE_URI = 'sqlite:///northcromo.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desabilitar tracking de modificações

# Inicializa o SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

# Variável para garantir que a conexão seja testada apenas uma vez
connection_tested = False

# Função para testar a conexão
def test_db_connection():
    global connection_tested
    if not connection_tested:  # Teste a conexão apenas uma vez
        try:
            with engine.connect() as con:
                con.execute(text('SELECT 1'))  # Query simples para testar a conexão
            print("Conexão com o banco de dados bem-sucedida!")
            connection_tested = True  # Marca que a conexão foi testada
        except Exception as e:
            print(f"Erro ao conectar com o banco de dados: {e}")

# Testa a conexão no início, quando o app é executado
test_db_connection()

# Inicializa Migrate para gerenciar migrations (opcional)
migrate = Migrate(app, db)

# Registra blueprints
from auth import auth_blueprint
from users import users_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(users_blueprint, url_prefix='/users')

# Ponto de entrada
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
