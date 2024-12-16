// src/pages/Cliente.tsx
import React, { useEffect, useState } from 'react';
import { getClientes } from '../api/clientes';

interface Cliente {
  id: number;
  nome: string;
  email: string;
}

// Exportação padrão (com default)
const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchClientes = async () => {
      try {
        const data = await getClientes();
        setClientes(data);
      } catch (error) {
        setError('Falha ao carregar os clientes.');
      } finally {
        setLoading(false);
      }
    };

    fetchClientes();
  }, []);

  if (loading) {
    return <div>Carregando...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

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

export default Cliente;  // Aqui é exportação padrão
