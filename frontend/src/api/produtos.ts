// src/api/produtos.ts
import { fetchAPI } from './index';

// Função para obter a lista de produtos
export const getProdutos = async () => {
    return fetchAPI('/produtos');
};

// Função para criar um novo produto
export const createProduto = async (produtoData: any) => {
    return fetchAPI('/produtos', 'POST', produtoData);
};

// Função para atualizar um produto
export const updateProduto = async (produtoId: number, produtoData: any) => {
    return fetchAPI(`/produtos/${produtoId}`, 'PUT', produtoData);
};

// Função para deletar um produto
export const deleteProduto = async (produtoId: number) => {
    return fetchAPI(`/produtos/${produtoId}`, 'DELETE');
};
