// src/api/clientes.ts
import { fetchAPI } from './index'; // Importando a função fetchAPI
import { Cliente } from '../types/Cliente';

// Variável para a URL base do cliente
const url_cliente = 'https://northcromocontrole.com.br/api/cliente';

// URL para listar tourl_clientedos os clientes
const url_listar_clientes = `${url_cliente}/`;  // Usando / no final

// URL para criar um novo cliente
const url_criar_cliente = `${url_cliente}/clientes`;  // Usando /clientes

// Função para listar todos os clientes
export const listarClientes = async (): Promise<Cliente[]> => {
  try {
    const response = await fetch(url_listar_clientes, {
      method: 'GET', // Requisição GET para listar clientes
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text(); // Captura texto de erro do backend
      throw new Error(`Erro ao listar clientes: ${errorText}`);
    }

    const clientes = await response.json();
    console.log('Lista de clientes:', clientes);
    return clientes; // Retorna a lista de clientes
  } catch (error) {
    console.error('Falha ao listar clientes:', error);
    throw error;
  }
};

// Função para enviar cliente para o backend
export const enviarParaBackend = async (cliente: Cliente) => {
  try {
    // Ajusta os dados para enviar conforme os campos esperados pelo backend
    const clienteParaEnviar = {
      nome_cliente: cliente.nome_cliente,  // Nome do cliente
      email_funcionario: cliente.email_funcionario,  // Email do cliente
      telefone_cliente: cliente.telefone_cliente,  // Telefone do cliente
      endereco_cliente: cliente.endereco_cliente,  // Endereço do cliente
      num_cliente: cliente.num_cliente,  // Número do cliente (se necessário)
      bairro_cliente: cliente.bairro_cliente,  // Bairro do cliente (se necessário)
      cidade_cliente: cliente.cidade_cliente,  // Cidade do cliente (se necessário)
      uf_cliente: cliente.uf_cliente,  // UF do cliente (se necessário)
      cep_cliente: cliente.cep_cliente,  // CEP do cliente (se necessário)
      whatsapp_cliente: cliente.whatsapp_cliente,  // WhatsApp do cliente (se necessário)
      telefone_rec_cliente: cliente.telefone_rec_cliente,  // Telefone de referência
      fornecedor_cliente: cliente.fornecedor_cliente,  // Fornecedor do cliente (se necessário)
      acao: cliente.acao,  // Ação do cliente (se necessário)
      tipo_cliente: cliente.tipo_cliente,  // Tipo de cliente
      doc_cliente: cliente.doc_cliente || ""  // Se 'doc_cliente' for null, substitua por uma string vazia
    };

    // Verificar se o tipo_cliente está vazio ou nulo antes de enviar
    if (!cliente.tipo_cliente) {
      cliente.tipo_cliente = 'default'; // Substitua 'default' por um valor adequado ou obrigatório
    }

    console.log('Enviando ao backend:', cliente);

    // Envia os dados para o backend
    const response = await fetch(url_criar_cliente, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(clienteParaEnviar),  // Envia os dados ajustados
    });

    if (!response.ok) {
      const errorText = await response.text();  // Captura texto de erro do backend
      throw new Error(`Erro ao enviar para o backend: ${errorText}`);
    }

    const result = await response.json();
    console.log('Resposta do servidor:', result);
    return result; // Retorna a resposta do backend
  } catch (error) {
    console.error('Falha ao enviar para backend:', error);
  }
};

// Função para atualizar um cliente no backend
export const editarClienteNoBackend = async (clienteId: number, clienteData: Cliente): Promise<any> => {
  try {
    console.log('Atualizando cliente no backend:', clienteData);

    const response = await fetch(`${url_criar_cliente}/${clienteId}`, {
      method: 'PUT', // Usando o método PUT para atualização
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(clienteData), // Envia os dados atualizados do cliente
    });

    if (!response.ok) {
      const errorText = await response.text(); // Captura texto de erro do backend
      console.error('Erro ao editar cliente no backend:', errorText);
      throw new Error(`Erro ao editar cliente no backend: ${errorText}`);
    }

    const result = await response.json();
    console.log('Resposta do servidor:', result);
    return result; // Retorna a resposta do backend
  } catch (error) {
    console.error('Falha ao editar cliente no backend:', error);
    throw error; // Lança o erro para que o chamador possa tratá-lo
  }
};

// Função para deletar um cliente no backend
export const deleteCliente = async (clienteId: number) => {
  const response = await fetch(`${url_criar_cliente}/${clienteId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Erro ao deletar cliente');
  }

  return await response.json();
};
