from ..models.componente import Componente
from ..main import db

# Listar todos os componentes
def list_componentes():
    componentes = Componente.query.all()  # Consulta todos os componentes
    return [componente.to_dict() for componente in componentes]

# Obter um componente específico
def get_componente(componente_id):
    componente = Componente.query.get(componente_id)  # Encontra o componente pelo ID
    return componente.to_dict() if componente else None

# Criar um novo componente
def create_componente(data):
    novo_componente = Componente(
        name=data['name'],
        usuario_id=data.get('usuario_id')  # Supondo que 'usuario_id' seja opcional
    )
    db.session.add(novo_componente)
    db.session.commit()
    return novo_componente.to_dict()

# Atualizar um componente existente
def update_componente(componente_id, data):
    componente = Componente.query.get(componente_id)
    if componente:
        componente.name = data.get('name', componente.name)
        componente.usuario_id = data.get('usuario_id', componente.usuario_id)
        db.session.commit()
        return componente.to_dict()
    return None

# Excluir um componente
def delete_componente(componente_id):
    componente = Componente.query.get(componente_id)
    if componente:
        db.session.delete(componente)
        db.session.commit()
        return True
    return False
