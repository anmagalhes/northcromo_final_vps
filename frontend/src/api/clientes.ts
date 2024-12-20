// src/api/clientes.ts
import { fetchAPI } from './index'; // Importando a função fetchAPI
import { Cliente } from '../types/Cliente';

// Função para obter a lista de clientes
export const getClientes = async () => {
    return fetchAPI('/api/cliente');
};

// Função para atualizar os dados de um cliente
export const updateCliente = async (clienteId: number, clienteData: any) => {
    try {
        const response = await fetch(`/api/cliente/${clienteId}`, {
            method: 'PUT', // Usando o método PUT para atualizar
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clienteData), // Envia os dados atualizados do cliente
        });

        // Verifica se a resposta foi bem-sucedida
        if (!response.ok) {
            throw new Error('Erro ao atualizar o cliente');
        }

        const result = await response.json();
        return result; // Retorna a resposta do backend (geralmente os dados atualizados ou uma confirmação)
    } catch (error) {
        console.error('Erro ao atualizar cliente no backend:', error);
        return { success: false }; // Caso haja erro, retorna um objeto com sucesso falso
    }
};

// Função para deletar um cliente
export const deleteCliente = async (clienteId: number) => {
    return fetchAPI(`/api/cliente/${clienteId}`, 'DELETE');
};

// Função para enviar cliente para o backend
export const enviarParaBackend = async (cliente: Cliente) => {
  try {
    console.log('Enviando cliente para o backend:', cliente); // Log para ver os dados enviados

    const response = await fetch('https://northcromocontrole.com.br/api/cliente', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(cliente),
    });

    if (!response.ok) {
      const errorText = await response.text(); // Pegue a resposta de erro do backend
      console.error('Erro ao enviar para o backend:', errorText);
      throw new Error(`Erro ao enviar cliente para o backend: ${errorText}`);
    }

    const result = await response.json();
    console.log('Resposta do servidor:', result);
    return result;
  } catch (error) {
    console.error('Falha ao enviar cliente para o backend:', error);
  }
};
  

