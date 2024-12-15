// src/api/clientes.ts
import { fetchAPI } from './index';

// Função para obter a lista de clientes
export const getClientes = async () => {
    return fetchAPI('/clientes');
};

// Função para criar um novo cliente
export const createCliente = async (clienteData: any) => {
    return fetchAPI('/clientes', 'POST', clienteData);
};

// Função para atualizar os dados de um cliente
export const updateCliente = async (clienteId: number, clienteData: any) => {
    return fetchAPI(`/clientes/${clienteId}`, 'PUT', clienteData);
};

// Função para deletar um cliente
export const deleteCliente = async (clienteId: number) => {
    return fetchAPI(`/clientes/${clienteId}`, 'DELETE');
};
