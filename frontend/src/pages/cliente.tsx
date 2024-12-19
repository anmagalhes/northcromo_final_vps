// src/pages/cliente.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';
import ClienteList from 'src/components/ClienteList/ClienteList';
import { salva_component } from 'src/utils';

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);

  // Função para excluir um cliente
  const handleDeleteCliente = (id: number) => {
    // Atualiza a lista de clientes após excluir um cliente
    setClientes((prevState) => prevState.filter((cliente) => cliente.id !== id));
    salva_component('clientes', clientes);  // Salva a lista de clientes atualizada (adapte conforme sua lógica)
  };

  // Simulação de adição de cliente para o exemplo
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    setClientes([...clientes, novoCliente]);
    salva_component('clientes', [...clientes, novoCliente]);  // Salva a lista após adicionar um novo cliente
  };

  return (
    <div>
      <h1>Gestão de Clientes</h1>
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientePage;
