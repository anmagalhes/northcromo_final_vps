// src/pages/ClientePage.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from 'src/types/Cliente';  // O tipo Cliente
import ClienteForm from 'src/components/ClienteForm/ClienteForm';  // Importando o formulário
import ClienteList from 'src/components/ClienteList/ClienteList';  // Componente para listar os clientes
import { salva_component } from 'src/utils';  // Função de salvar cliente

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Lista de clientes

  // Função chamada quando um novo cliente é adicionado
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    setClientes((prevClientes) => {
      const updatedClientes = [...prevClientes, novoCliente];
      salva_component('clientes', updatedClientes);  // Salva a lista de clientes atualizada
      return updatedClientes;
    });
  };

  // Carregar os clientes do localStorage ao iniciar
  useEffect(() => {
    const clientesSalvos = JSON.parse(localStorage.getItem('clientes') || '[]');
    setClientes(clientesSalvos);
  }, []);

  return (
    <div>
      <header>
        <h1>Bem-vindo à página de Clientes</h1>
        <p>Aqui você pode ver todos os seus clientes e adicionar novos.</p>
      </header>

      {/* Formulário para adicionar um novo cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />

      <hr />

      {/* Exibindo a lista de clientes */}
      <ClienteList clientes={clientes} />

      {/* Outras informações extras */}
      <section>
        <h2>Outras informações</h2>
        <p>Você pode adicionar mais funcionalidades aqui, como editar ou remover clientes.</p>
      </section>
    </div>
  );
};

export default ClientePage;

