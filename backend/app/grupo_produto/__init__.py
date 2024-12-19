from flask import Blueprint

# Cria o blueprint para o módulo de funcionários
grupo_produto_blueprint = Blueprint('grupo_produto', __name__)

# Importa as rotas para registrá-las no blueprint
from . import routes