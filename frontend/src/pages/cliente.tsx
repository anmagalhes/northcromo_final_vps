// src/pages/Cliente.tsx
import React, { useEffect, useState } from 'react';
import { getClientes, deleteCliente } from '../api/clientes';  // Funções de API
import ClienteForm from '../components/ClienteForm/ClienteForm';  // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList';  // Lista de Clientes
import { Cliente } from '../types/Cliente';  // Certificando-se de usar o tipo correto

// Tipos para melhorar a tipagem de erro e estados
type ErrorMessage = string | null;
type LoadingState = boolean;

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);
  const [loading, setLoading] = useState<LoadingState>(true);
  const [error, setError] = useState<ErrorMessage>(null);

  // Função para carregar os clientes, com tratamento de erros e loading
  useEffect(() => {
    const fetchClientes = async () => {
      setLoading(true);
      try {
        const data = await getClientes();  // Função de API para obter clientes
        setClientes(data);
      } catch (err) {
        setError('Falha ao carregar os clientes.');
      } finally {
        setLoading(false);
      }
    };

    fetchClientes();
  }, []);  // O array vazio faz com que isso seja executado apenas uma vez, quando o componente for montado

  // Função para excluir um cliente
  const handleDeleteCliente = async (id: number) => {
    setLoading(true); // Mudar para loading true durante a requisição
    try {
      await deleteCliente(id);  // Exclui o cliente usando a API
      // Filtra o cliente removido da lista
      setClientes((prevClientes) => prevClientes.filter(cliente => cliente.id !== id));
    } catch (err) {
      setError('Falha ao excluir o cliente.');
    } finally {
      setLoading(false);  // Desativa o loading quando a requisição for completada
    }
  };

  // Função para adicionar um novo cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    setClientes((prevClientes) => [...prevClientes, novoCliente]); // Atualiza a lista de clientes
  };

  if (loading) {
    return <div>Carregando clientes...</div>;  // Mensagem de loading
  }

  return (
    <div>
      <h1>Clientes CRISTIANE</h1>
      
      {/* Exibição de erro, se houver */}
      {error && <div style={{ color: 'red' }}>{error}</div>}

      {/* Formulário de cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />

      {/* Lista de clientes com botão de deletar */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientePage;
