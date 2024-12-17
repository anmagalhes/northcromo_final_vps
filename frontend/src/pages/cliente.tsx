// src/pages/Cliente.tsx
import React, { useEffect, useState } from 'react';
import { getClientes, deleteCliente } from '../api/clientes';  // Funções para buscar e excluir clientes
import ClienteForm from '../components/ClienteForm/ClienteForm';  // Importando o formulário
import ClienteList from '../components/ClienteList/ClienteList';  // Importando a lista de clientes
import { Cliente } from '../types/Cliente';  // Importando o tipo Cliente do arquivo de tipos

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

  const handleDeleteCliente = async (id: number) => {
    try {
      await deleteCliente(id);
      setClientes(clientes.filter(cliente => cliente.id !== id));
    } catch (error) {
      setError('Falha ao excluir o cliente.');
    }
  };

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

// Exportando o componente usando export default
export default Cliente;  // Exportação padrão
