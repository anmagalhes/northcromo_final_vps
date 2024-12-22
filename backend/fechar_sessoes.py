from app import create_app, db  # Ou importe o db e a função de criar o app

def fechar_sessoes():
    """Fechar todas as sessões ativas do SQLAlchemy"""
    with app.app_context():  # Garante que estamos dentro do contexto da aplicação
        db.session.remove()  # Remove a sessão ativa
        print("Sessões fechadas com sucesso.")

def abrir_sessao():
    """Abrir a sessão do SQLAlchemy"""
    app = create_app()  # Cria a instância do app Flask
    with app.app_context():  # Garante que estamos no contexto da aplicação
        # A sessão já é automaticamente aberta dentro do contexto do app
        db.session.begin()  # Isso inicia uma nova transação
        print("Sessão aberta com sucesso!")
        
# Chama a função para abrir a sessão
if __name__ == "__main__":
    abrir_sessao()  # Chama a função para abrir a sessão
