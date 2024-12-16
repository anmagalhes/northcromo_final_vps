// src/pages/ClientesPage.tsx
import React, { useEffect, useState } from 'react';
import { getClientes, deleteCliente } from '../api/clientes';  // Funções para buscar e excluir clientes
import ClienteForm from '../components/ClienteForm/ClienteForm';  // Importando o formulário
import ClienteList from '../components/ClienteList/ClienteList';  // Importando a lista de clientes
import { Cliente } from '../types/Cliente'; 

interface Cliente {
  id: number;
  nome: string;
  email: string;
}

const ClientesPage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Carregar clientes quando o componente for montado
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

  // Função para excluir um cliente
  const handleDeleteCliente = async (id: number) => {
    try {
      await deleteCliente(id);
      setClientes(clientes.filter(cliente => cliente.id !== id));  // Remove o cliente da lista
    } catch (error) {
      setError('Falha ao excluir o cliente.');
    }
  };

  // Função para adicionar um cliente à lista local
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    setClientes(prevClientes => [...prevClientes, novoCliente]);
  };

  if (loading) {
    return <div>Carregando clientes...</div>;
  }

  return (
    <div>
      <h1>Clientes</h1>

      {/* Exibir mensagem de erro */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Componente de formulário para adicionar cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />

      {/* Componente de lista de clientes */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientesPage;
