# Exemplo de função no services.py
from ..models.grupo_produto import Grupo_Produto
from app import db
from app.grupo_produto import Grupo_Produto

grupo_produto_schema = Grupo_Produto()
grupo_produtos_schema = Grupo_Produto(many=True)

def list_grupo_produtos():
    grupo_produtos = Grupo_Produto.query.all()  # Consulta todos os grupos de produtos
    return grupo_produtos_schema.dump(grupo_produtos)

def get_grupo_produto(grupo_produto_id):
    grupo_produto = Grupo_Produto.query.get(grupo_produto_id)
    if grupo_produto:
        return grupo_produto_schema.dump(grupo_produto)
    return None

def create_grupo_produto(data):
    novo_grupo_produto = grupo_produto_schema.load(data)  # Carrega os dados do schema
    db.session.add(novo_grupo_produto)
    db.session.commit()
    return grupo_produto_schema.dump(novo_grupo_produto)

def update_grupo_produto(grupo_produto_id, data):
    grupo_produto = Grupo_Produto.query.get(grupo_produto_id)
    if grupo_produto:
        grupo_produto_schema.load(data, instance=grupo_produto, partial=True)
        db.session.commit()
        return grupo_produto_schema.dump(grupo_produto)
    return None

def delete_grupo_produto(grupo_produto_id):
    grupo_produto = Grupo_Produto.query.get(grupo_produto_id)
    if grupo_produto:
        db.session.delete(grupo_produto)
        db.session.commit()
        return True
    return False
