from flask import Blueprint

# Cria o blueprint para o módulo defeitos
foto_recebimento_blueprint = Blueprint('foto_recebimento', __name__)

# Importa as rotas que serão registradas no blueprint
from . import routes