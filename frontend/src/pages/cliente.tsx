// src/pages/Cliente.tsx
import React, { useEffect, useState } from 'react';
import { getClientes, deleteCliente } from '../api/clientes';
import ClienteForm from '../components/ClienteForm/ClienteForm';
import ClienteList from '../components/ClienteList/ClienteList';
import { Cliente } from '../types/Cliente';  // Importando corretamente o tipo 'Cliente'

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Usando o tipo correto
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

  const handleDeleteCliente = async (id: number) => {
    try {
      await deleteCliente(id);
      setClientes(clientes.filter(cliente => cliente.id !== id));
    } catch (error) {
      setError('Falha ao excluir o cliente.');
    }
  };

  // A função handleClienteAdicionado recebe um 'Cliente' corretamente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    setClientes(prevClientes => [...prevClientes, novoCliente]);
  };

  if (loading) {
    return <div>Carregando clientes...</div>;
  }

  return (
    <div>
      <h1>Clientes</h1>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientePage;
