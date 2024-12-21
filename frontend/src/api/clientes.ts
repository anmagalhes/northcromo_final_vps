// src/api/clientes.ts
import { fetchAPI } from './index'; // Importando a função fetchAPI
import { Cliente } from '../types/Cliente';

// Variável para a URL base do cliente
const url_cliente = 'https://northcromocontrole.com.br/api/cliente';

// Função para enviar cliente para o backend
const enviarParaBackend = async (novoCliente: Cliente) => {
  try {
    // Verificar se o tipo_cliente está vazio ou nulo
    if (!novoCliente.tipo_cliente) {
      novoCliente.tipo_cliente = 'default'; // Substitua 'default' por um valor adequado ou obrigatório
    }

    // Agora que o tipo_cliente está garantido, envie os dados para a API
    const response = await fetch('https://northcromocontrole.com.br/api/cliente', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(novoCliente),  // Enviar os dados
    });

    const result = await response.json();
    if (response.ok) {
      console.log('Cliente enviado com sucesso', result);
    } else {
      throw new Error(result.error || 'Erro desconhecido');
    }
  } catch (error) {
    console.error('Falha ao enviar cliente para o backend:', error);
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

// src/api/clientes.ts
// src/api/clientes.ts
export const deleteCliente = async (clienteId: number) => {
  const response = await fetch(`${url_cliente}/${clienteId}`, {
    method: 'DELETE',
  });

  if (!response.ok) {
    throw new Error('Erro ao deletar cliente');
  }

  return await response.json();
};


  

