from app import app  # Importando a instância do Flask que está em app.py

# Cria a instância da aplicação Flask
app = create_app()

if __name__ == "__main__":
    app.run()