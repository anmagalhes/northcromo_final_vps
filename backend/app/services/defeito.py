from app.models.defeito_model import Defeito

# Função para listar todos os defeitos
def list_defeitos():
    defeitos = Defeito.query.all()  # Consulta todos os defeitos no banco de dados
    return [defeito.to_dict() for defeito in defeitos]  # Supondo que você tenha um método to_dict()

# Função para obter um defeito específico
def get_defeito(defeito_id):
    defeito = Defeito.query.get(defeito_id)  # Busca o defeito pelo ID
    return defeito.to_dict() if defeito else None

# Função para criar um novo defeito
def create_defeito(data):
    novo_defeito = Defeito(**data)  # Cria um objeto Defeito com os dados recebidos
    db.session.add(novo_defeito)  # Adiciona ao banco
    db.session.commit()  # Commit da transação
    return novo_defeito.to_dict()

# Função para atualizar um defeito existente
def update_defeito(defeito_id, data):
    defeito = Defeito.query.get(defeito_id)  # Busca o defeito pelo ID
    if defeito:
        for key, value in data.items():
            setattr(defeito, key, value)  # Atualiza os atributos do defeito
        db.session.commit()  # Commit da transação
        return defeito.to_dict()
    return None

# Função para deletar um defeito
def delete_defeito(defeito_id):
    defeito = Defeito.query.get(defeito_id)  # Busca o defeito pelo ID
    if defeito:
        db.session.delete(defeito)  # Deleta o defeito
        db.session.commit()  # Commit da transação
        return True
    return False