from app.main_validado import app  # Seu app Flask
from models import db  # Instância do banco de dados
from app.models.user import User  # Importe o modelo 'Usuarios'

# Função para deletar a tabela 'usuarios'
def deletar_tabela():
    with app.app_context():
        # Deleta a tabela 'usuarios'
        db.engine.execute('DROP TABLE IF EXISTS usuarios CASCADE')
        print("Tabela 'usuarios' deletada com sucesso!")

# Chamando a função
if __name__ == "__main__":
    deletar_tabela()
