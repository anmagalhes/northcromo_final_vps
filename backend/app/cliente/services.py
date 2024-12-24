# app/cliente/services.py
from flask import jsonify, g 
from ..models.cliente import Cliente
from app import db
from app.schemas.cliente import ClienteSchema  # Importação relativa

# Instância do schema
cliente_schema = ClienteSchema()  # Para operações com um único cliente

# Listar todos os clientes
def list_clientes():
  #  clientes = Cliente.query.all()  # Consulta todos os clientes
 # return [cliente_schema.dump(cliente) for cliente in clientes]  # Serializa e retorna a lista de clientes
 return [{"id": 1, "nome": "John Doe"}, {"id": 2, "nome": "Jane Doe"}]

# Obter um cliente específico
def get_cliente(id):
    cliente = Cliente.query.get(id)  # Encontra o cliente pelo ID
    return cliente_schema.dump(cliente) if cliente else None  # Serializa o cliente ou retorna None

# Função para criar um novo cliente
def create_cliente(data):
    try:
        # Validando se todos os campos obrigatórios estão presentes
        if not data.get('nome_cliente') or not data.get('tipo_cliente') or not data.get('doc_cliente'):
            raise ValueError("Os campos tipo_cliente, nome_cliente e doc_cliente são obrigatórios!")

        # Atribuindo o ID do usuário (como admin, por exemplo) para o cliente
        usuario_id = data.get('usuario_id', 1)  # 1 é o ID do usuário admin, ou ID padrão

        # Criando o cliente com os dados fornecidos
        cliente = Cliente(
            tipo_cliente=data.get('tipo_cliente'),
            nome_cliente=data.get('nome_cliente'),
            doc_cliente=data.get('doc_cliente'),
            endereco_cliente=data.get('endereco_cliente'),
            num_cliente=data.get('num_cliente'),
            bairro_cliente=data.get('bairro_cliente'),
            cidade_cliente=data.get('cidade_cliente'),
            uf_cliente=data.get('uf_cliente'),
            cep_cliente=data.get('cep_cliente'),
            telefone_cliente=data.get('telefone_cliente'),
            telefone_rec_cliente=data.get('telefone_rec_cliente'),
            whatsapp_cliente=data.get('whatsapp_cliente'),
            fornecedor_cliente=data.get('fornecedor_cliente'),
            email_funcionario=data.get('email_funcionario'),
            acao=data.get('acao'),
            usuario_id=usuario_id  # Forçando o envio do usuario_id
        )

        # Adicionando o cliente à sessão do banco de dados
        g.db_session.add(cliente)
        g.db_session.commit()  # Commitando a transação no banco de dados

        # Serializando e retornando o cliente criado
        return cliente_schema.dump(cliente)  # Serializando o objeto cliente para dicionário

    except ValueError as e:
        # Retornar erro específico de validação
        g.db_session.rollback()  # Em caso de erro, faz rollback
        return {"error": str(e)}, 400  # Retornando erro com código 400
    
    except Exception as e:
        # Tratar exceções inesperadas
        g.db_session.rollback()
        return {"error": f"Erro ao criar cliente: {str(e)}"}, 500  # Retornando erro com código 500
    

# Atualizar um cliente existente
def update_cliente(id, data):
    cliente = Cliente.query.get(id)
    if cliente:
        # Atualiza cada campo com os dados recebidos ou mantém o valor existente
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
        db.session.commit() # Persiste as mudanças no banco
        return cliente_schema.dump(cliente)  # Retorna o cliente atualizado serializado
    return None  # Retorna None se o cliente não for encontrado

# Excluir um cliente
def delete_cliente(id):
    cliente = Cliente.query.get(id)
    if cliente:
        db.session.delete(cliente)
        db.session.commit() # Persiste a exclusão no banco
        return True  # Cliente deletado com sucesso
    return False # Cliente não encontrado
