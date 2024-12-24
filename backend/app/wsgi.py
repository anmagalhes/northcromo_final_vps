# wsgi.py

from backend.app.main import create_app

# Cria a instância da aplicação com a função 'create_app'
#application = create_app()

# O Gunicorn ou qualquer outro servidor WSGI vai procurar por esta variável 'application' para rodar a aplicação
