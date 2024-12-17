# checklist_recebimento/__init__.py
from flask import Blueprint

# Cria o blueprint para checklist_recebimento
checklist_recebimento_blueprint = Blueprint('checklist_recebimento', __name__)

# Importa as rotas que serão registradas no blueprint
from . import routes

