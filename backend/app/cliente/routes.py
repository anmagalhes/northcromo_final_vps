from flask import jsonify, request
from . import cliente_blueprint
from .services import list_clientes, get_cliente, create_cliente, update_cliente, delete_cliente
from app.schemas.cliente import ClienteSchema

# Instância do schema teste
cliente_schema = ClienteSchema()  # Para operações com um único cliente
clientes_schema = ClienteSchema(many=True)  # Para listar múltiplos clientes

# Rota para listar todos os clientes
@cliente_blueprint.route('/', methods=['GET'])
def get_all_clientes():
    clientes = list_clientes()  # Chama a função que lista os clientes
    return jsonify(clientes), 200

# Rota para pegar detalhes de um cliente específico
@cliente_blueprint.route('/<int:id>', methods=['GET'])
def get_cliente_details(id):
    cliente = get_cliente(id)  # Chama a função que obtém os detalhes do cliente
    if cliente:
        return jsonify(cliente), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404

# Rota para criar um novo cliente
def create_cliente(data):
    try:
        # Validando se todos os campos obrigatórios estão presentes
        if not data.get('tipo_cliente') or not data.get('nome_cliente') or not data.get('doc_cliente'):
            raise ValueError("Os campos tipo_cliente, nome_cliente e doc_cliente são obrigatórios!")

        # Atribuindo o ID do usuário (usuário admin ou o que for necessário)
        usuario_id = data.get('usuario_id', 1)  # ID do usuário admin, caso não seja enviado

        # Criando o cliente
        cliente = Cliente(
            tipo_cliente=data['tipo_cliente'],
            nome_cliente=data['nome_cliente'],
            doc_cliente=data['doc_cliente'],
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
            usuario_id=usuario_id  # Atribuindo o usuário ao cliente
        )

        # Adicionando o cliente à sessão do banco de dados
        g.db_session.add(cliente)
        g.db_session.commit()  # Commitando a transação

        # Retornando o cliente com os dados serializados
        return cliente.to_json()  # Usando o método to_json para retorno

    except ValueError as e:
        # Retornar erro específico de validação
        g.db_session.rollback()  # Rollback em caso de erro
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        # Erro geral
        g.db_session.rollback()  # Rollback em caso de erro
        return jsonify({"error": f"Erro ao criar cliente: {str(e)}"}), 500

# Rota para atualizar um cliente
@cliente_blueprint.route('/<int:id>', methods=['PUT'])
def update_cliente_details(id):
    data = request.get_json()

    # Verifica se o cliente existe antes de tentar atualizar
    cliente = get_cliente(id)
    if not cliente:
        return jsonify({"message": "Cliente não encontrado!"}), 404

    # Valida os dados do cliente com o Marshmallow
    errors = cliente_schema.validate(data)
    if errors:
        return jsonify({"error": "Dados inválidos", "details": errors}), 400

    # Atualiza os dados do cliente
    updated_cliente = update_cliente(id, data)
    if updated_cliente:
        return jsonify(updated_cliente), 200
    return jsonify({"message": "Erro ao atualizar cliente"}), 500

# Rota para deletar um cliente
@cliente_blueprint.route('/<int:id>', methods=['DELETE'])
def delete_cliente_by_id(id):
    if delete_cliente(id):
        return jsonify({"message": "Cliente excluído com sucesso!"}), 200
    return jsonify({"message": "Cliente não encontrado!"}), 404
