// src/pages/Cliente.tsx
import React, { useEffect, useState } from 'react';
import { getClientes } from '../api/clientes';  // Importa a função de clientes

interface Cliente {
  id: number;
  nome: string;
  email: string;
}

export const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]); // Estado para armazenar os clientes
  const [loading, setLoading] = useState<boolean>(true);   // Estado para controlar o carregamento
  const [error, setError] = useState<string | null>(null);  // Estado para mostrar erros

  useEffect(() => {
    // Função para carregar os clientes da API
    const fetchClientes = async () => {
      try {
        const data = await getClientes();
        setClientes(data); // Armazena os clientes no estado
      } catch (error) {
        setError('Falha ao carregar os clientes.');
      } finally {
        setLoading(false); // Termina o carregamento
      }
    };

    fetchClientes(); // Chama a função de requisição
  }, []); // Executa apenas uma vez quando o componente é montado

  // Exibe uma mensagem de carregamento
  if (loading) {
    return <div>Carregando...</div>;
  }

  // Exibe mensagem de erro se houver
  if (error) {
    return <div>{error}</div>;
  }

  // Exibe a lista de clientes
  return (
    <div>
      <h1>Lista de Clientes</h1>
      <ul>
        {clientes.map(cliente => (
          <li key={cliente.id}>
            <strong>{cliente.nome}</strong> - {cliente.email}
          </li>
        ))}
      </ul>
    </div>
  );
};
