from ..models.cliente import Cliente
from app import db

# Listar todos os clientes
def list_clientes():
  #  clientes = Cliente.query.all()  # Consulta todos os clientes
# return [cliente.to_dict() for cliente in clientes]
 return [{"id": 1, "nome": "John Doe"}, {"id": 2, "nome": "Jane Doe"}]

# Obter um cliente específico
def get_cliente(id):
    cliente = Cliente.query.get(id)  # Encontra o cliente pelo ID
    return cliente.to_dict() if cliente else None

# Criar um novo cliente
def create_cliente(data):
    cliente = Cliente(
        tipo_cliente=data['tipo_cliente'],
        nome_cliente=data['nome_cliente'],
        doc_cliente=data['doc_cliente'],
        endereco_cliente=data['endereco_cliente'],
        num_cliente=data['num_cliente'],
        bairro_cliente=data['bairro_cliente'],
        cidade_cliente=data['cidade_cliente'],
        uf_cliente=data['uf_cliente'],
        cep_cliente=data['cep_cliente'],
        telefone_cliente=data['telefone_cliente'],
        telefone_rec_cliente=data.get('telefone_rec_cliente'),
        whatsapp_cliente=data.get('whatsapp_cliente'),
        fornecedor_cliente=data['fornecedor_cliente'],
        email_funcionario=data.get('email_funcionario'),
        acao=data.get('acao'),
    )
    db.session.add(cliente)
    db.session.commit()
    return cliente.to_dict()

# Atualizar um cliente existente
def update_cliente(id, data):
    cliente = Cliente.query.get(id)
    if cliente:
        cliente.tipo_cliente = data.get('tipo_cliente', cliente.tipo_cliente)
        cliente.nome_cliente = data.get('nome_cliente', cliente.nome_cliente)
        cliente.doc_cliente = data.get('doc_cliente', cliente.doc_cliente)
        cliente.endereco_cliente = data.get('endereco_cliente', cliente.endereco_cliente)
        cliente.num_cliente = data.get('num_cliente', cliente.num_cliente)
        cliente.bairro_cliente = data.get('bairro_cliente', cliente.bairro_cliente)
        cliente.cidade_cliente = data.get('cidade_cliente', cliente.cidade_cliente)
        cliente.uf_cliente = data.get('uf_cliente', cliente.uf_cliente)
        cliente.cep_cliente = data.get('cep_cliente', cliente.cep_cliente)
        cliente.telefone_cliente = data.get('telefone_cliente', cliente.telefone_cliente)
        cliente.telefone_rec_cliente = data.get('telefone_rec_cliente', cliente.telefone_rec_cliente)
        cliente.whatsapp_cliente = data.get('whatsapp_cliente', cliente.whatsapp_cliente)
        cliente.fornecedor_cliente = data.get('fornecedor_cliente', cliente.fornecedor_cliente)
        cliente.email_funcionario = data.get('email_funcionario', cliente.email_funcionario)
        cliente.acao = data.get('acao', cliente.acao)
        db.session.commit()
        return cliente.to_dict()
    return None

# Excluir um cliente
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit()
        return True
    return False
