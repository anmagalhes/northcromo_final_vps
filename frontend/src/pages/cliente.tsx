// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from 'src/types/Cliente';
import ClienteForm from 'src/components/ClienteForm/ClienteForm';
import ClienteList from 'src/components/ClienteList/ClienteList';
import { salva_component } from 'src/utils';

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);

  // Função para excluir um cliente
  const handleDeleteCliente = (id: number) => {
    const updatedClientes = clientes.filter((cliente) => cliente.id !== id);
    setClientes(updatedClientes);  // Atualiza o estado com a lista sem o cliente excluído

    // Salva a lista de clientes atualizada no localStorage
    salva_component('clientes', updatedClientes);  // Agora salva corretamente
  };

  // Função para adicionar um novo cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    const updatedClientes = [...clientes, novoCliente];
    setClientes(updatedClientes);  // Atualiza o estado com o novo cliente

    // Salva a lista de clientes após adicionar o novo cliente no localStorage
    salva_component('clientes', updatedClientes);  // Agora salva corretamente
  };

  // Carregar a lista de clientes do localStorage ao iniciar a página
  useEffect(() => {
    const storedClientes = localStorage.getItem('clientes');
    if (storedClientes) {
      setClientes(JSON.parse(storedClientes));  // Carrega os clientes armazenados no localStorage
    }
  }, []);

  return (
    <div>
      <h1>Gestão de Clientes</h1>

      {/* Formulário de cadastro de cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />

      {/* Lista de clientes */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientePage;
