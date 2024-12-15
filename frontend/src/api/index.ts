// src/api/index.ts

const API_URL = '/api';  // Base URL, pode ser alterada se necessário

// Função genérica para fazer requisições HTTP
export const fetchAPI = async (endpoint: string, method: string = 'GET', body?: any) => {
    const url = `${API_URL}${endpoint}`;
    
    const options: RequestInit = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };

    // Se houver corpo, adiciona ao corpo da requisição (usado em POST, PUT, etc.)
    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, options);
        if (!response.ok) {
            throw new Error(`Erro ao fazer requisição: ${response.statusText}`);
        }
        return await response.json();  // Retorna a resposta em JSON
    } catch (error) {
        console.error('Erro ao fazer requisição:', error);
        throw error;  // Lança o erro para ser tratado em outros lugares
    }
};
