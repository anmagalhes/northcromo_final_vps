from ..models.funcionario_model import Funcionario
# Função para listar todos os funcionários
def list_funcionarios():
    funcionarios = Funcionario.query.all()
    return [funcionario.to_dict() for funcionario in funcionarios]

# Função para obter um funcionário específico
def get_funcionario(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    return funcionario.to_dict() if funcionario else None

# Função para criar um novo funcionário
def create_funcionario(data):
    funcionario = Funcionario(
        nome=data['nome'],
        telefone=data['telefone'],
        email=data['email'],
        funcao=data['funcao'],
        setor=data['setor'],
        nivel_acesso=data['nivel_acesso'],
        acao=data.get('acao')
    )
    db.session.add(funcionario)
    db.session.commit()
    return funcionario.to_dict()

# Função para atualizar um funcionário
def update_funcionario(funcionario_id, data):
    funcionario = Funcionario.query.get(funcionario_id)
    if funcionario:
        funcionario.nome = data.get('nome', funcionario.nome)
        funcionario.telefone = data.get('telefone', funcionario.telefone)
        funcionario.email = data.get('email', funcionario.email)
        funcionario.funcao = data.get('funcao', funcionario.funcao)
        funcionario.setor = data.get('setor', funcionario.setor)
        funcionario.nivel_acesso = data.get('nivel_acesso', funcionario.nivel_acesso)
        funcionario.acao = data.get('acao', funcionario.acao)
        db.session.commit()
        return funcionario.to_dict()
    return None

# Função para excluir um funcionário
def delete_funcionario(funcionario_id):
    funcionario = Funcionario.query.get(funcionario_id)
    if funcionario:
        db.session.delete(funcionario)
        db.session.commit()
        return True
    return False
