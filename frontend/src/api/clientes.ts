// src/api/clientes.ts
import { fetchAPI } from './index'; // Importando a função fetchAPI
import { Cliente } from '../types/Cliente';

// Variável para a URL base do cliente
const url_cliente = 'https://northcromocontrole.com.br/api/cliente';

// Função para obter a lista de clientes
export const getClientes = async (): Promise<any> => {
  try {
    const response = await fetchAPI('/api/cliente');
    return response; // Retorna a resposta da API
  } catch (error) {
    console.error("Erro ao obter clientes:", error);
    throw new Error('Erro ao obter a lista de clientes');
  }
};

// Função para deletar um cliente
export const deleteCliente = async (clienteId: number): Promise<any> => {
  try {
    const response = await fetchAPI(`/api/cliente/${clienteId}`, 'DELETE');
    return response; // Retorna a resposta da API
  } catch (error) {
    console.error("Erro ao excluir cliente:", error);
    throw new Error('Erro ao excluir cliente');
  }
};

// Função para enviar cliente para o backend
export const enviarParaBackend = async (cliente: Cliente): Promise<any> => {
  try {
    console.log('Enviando cliente para o backend:', cliente);

    const response = await fetch(url_cliente, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(cliente),
    });

    if (!response.ok) {
      const errorText = await response.text(); // Captura texto de erro do backend
      console.error('Erro ao enviar para o backend:', errorText);
      throw new Error(`Erro ao enviar cliente para o backend: ${errorText}`);
    }

    const result = await response.json();
    console.log('Resposta do servidor:', result);
    return result; // Retorna a resposta do backend
  } catch (error) {
    console.error('Falha ao enviar cliente para o backend:', error);
    throw error; // Lança o erro para que o chamador possa tratá-lo
  }
};

// Função para atualizar um cliente no backend
export const editarClienteNoBackend = async (clienteId: number, clienteData: Cliente): Promise<any> => {
  try {
    console.log('Atualizando cliente no backend:', clienteData);

    const response = await fetch(`${url_cliente}/${clienteId}`, {
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

  

