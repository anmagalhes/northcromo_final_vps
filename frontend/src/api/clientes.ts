// src/api/clientes.ts
import { fetchAPI } from './index'; // Importando a função fetchAPI

// Função para obter a lista de clientes
export const getClientes = async () => {
    return fetchAPI('/api/cliente');
};

// Função para criar um novo cliente
export const createCliente = async (clienteData: any) => {
    try {
        const response = await fetch('/api/cliente', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(clienteData),
        });

        // Verifica se a resposta foi bem-sucedida
        if (!response.ok) {
            throw new Error('Erro ao criar o cliente');
        }

        const result = await response.json();
        return result; // { success: true } ou o que for retornado pelo seu backend
    } catch (error) {
        console.error('Erro ao enviar cliente para o backend:', error);
        return { success: false };
    }
};

// Função para atualizar os dados de um cliente
export const updateCliente = async (clienteId: number, clienteData: any) => {
    return fetchAPI(`/api/cliente/${clienteId}`, 'PUT', clienteData);
};

// Função para deletar um cliente
export const deleteCliente = async (clienteId: number) => {
    return fetchAPI(`/api/cliente/${clienteId}`, 'DELETE');
};

