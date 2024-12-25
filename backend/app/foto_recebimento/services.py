from ..models.foto_recebimento import FotoRecebimento

# Função para listar todas as fotos de recebimento
def list_fotos():
    fotos = FotoRecebimento.query.all()  # Retorna todas as fotos
    return [foto.to_dict() for foto in fotos]

# Função para pegar os detalhes de uma foto de recebimento específica
def get_foto(foto_id):
    foto = FotoRecebimento.query.get(foto_id)  # Busca uma foto pelo ID
    if foto:
        return foto.to_dict()
    return None

# Função para criar uma nova foto de recebimento
def create_foto(data):
    try:
        nova_foto = FotoRecebimento(
            id_ordem=data['id_ordem'],
            nome_foto=data['nome_foto'],
            recebimento_id=data['recebimento_id'],
            usuario_id=data.get('usuario_id')
        )
        db.session.add(nova_foto)
        db.session.commit()
        return nova_foto.to_dict()
    except Exception as e:
        db.session.rollback()
        return {"message": f"Erro ao criar foto: {str(e)}"}

# Função para atualizar os detalhes de uma foto de recebimento
def update_foto(foto_id, data):
    foto = FotoRecebimento.query.get(foto_id)
    if foto:
        foto.id_ordem = data.get('id_ordem', foto.id_ordem)
        foto.nome_foto = data.get('nome_foto', foto.nome_foto)
        foto.recebimento_id = data.get('recebimento_id', foto.recebimento_id)
        foto.usuario_id = data.get('usuario_id', foto.usuario_id)
        
        db.session.commit()
        return foto.to_dict()
    return None

# Função para excluir uma foto de recebimento
def delete_foto(foto_id):
    foto = FotoRecebimento.query.get(foto_id)
    if foto:
        db.session.delete(foto)
        db.session.commit()
        return True
    return False
