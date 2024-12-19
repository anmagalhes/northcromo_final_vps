// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from 'src/types/Cliente';  // Tipo Cliente
import ClienteForm from 'src/components/ClienteForm/ClienteForm';  // Formulário de Cliente
import ClienteList from 'src/components/ClienteList/ClienteList';  // Lista de Clientes
import Button from '../components/Button/Button';  // Componente de Botão
import { salva_component } from 'src/utils';  // Função de Salvamento

const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Estado para armazenar a lista de clientes

  // Carregar os clientes do localStorage quando a página for carregada
  useEffect(() => {
    const clientesSalvos = localStorage.getItem('clientes');
    if (clientesSalvos) {
      setClientes(JSON.parse(clientesSalvos));  // Carrega os dados para o estado
    }
  }, []);

  // Função para adicionar um cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    // Adiciona o novo cliente ao estado
    const updatedClientes = [...clientes, novoCliente];
    setClientes(updatedClientes);
    
    // Salva a lista de clientes no localStorage
    salva_component('clientes', updatedClientes);  // Salvando no localStorage
  };

  // Função para excluir um cliente
  const handleDeleteCliente = (id: number) => {
    const updatedClientes = clientes.filter((cliente) => cliente.id !== id);
    setClientes(updatedClientes);
    salva_component('clientes', updatedClientes);  // Salvando no localStorage após exclusão
  };

  return (
    <div>
      <h2>Gestão de Clientes</h2>
      
      {/* Formulário para adicionar um novo cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />
      
      {/* Lista de Clientes */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
      
      {/* Botão de ação (por exemplo, para algum outro propósito) */}
      <Button label="Clique aqui" onClick={() => alert('Ação de botão executada!')} />
    </div>
  );
};

export default Cliente;
