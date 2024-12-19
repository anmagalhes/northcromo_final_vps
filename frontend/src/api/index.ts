// Definir a URL base da API dependendo do ambiente
const API_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:5000/api'  // URL para desenvolvimento (Flask rodando localmente na porta 5000)
  : 'https://northcromocontrole.com.br/api;  // URL relativa para produção (quando o frontend e o backend estão no mesmo domínio)

export const fetchAPI = async (endpoint: string, method: string = 'GET', data: any = null) => {
  const options: RequestInit = {
    method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  if (data) {
    options.body = JSON.stringify(data);  // Se houver dados, adiciona ao corpo da requisição
  }

  try {
    const response = await fetch(`${API_URL}${endpoint}`, options);

    if (!response.ok) {
      throw new Error('Erro na requisição');
    }

    return await response.json();  // Retorna o corpo da resposta JSON
  } catch (error) {
    console.error('Erro ao fazer a requisição:', error);
    throw error;
  }
};

