// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from '../types/Cliente';  // Tipo Cliente
import ClienteForm from '../components/ClienteForm/ClienteForm';  // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList';  // Lista de Clientes
import Button from '../components/Button/Button';  // Componente de Botão
import { salva_component } from '../utils';  // Função de Salvamento

const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Estado para armazenar a lista de clientes

  // Carregar os clientes do localStorage quando a página for carregada
  useEffect(() => {
    const clientesSalvos = localStorage.getItem('clientes');
    if (clientesSalvos) {
      try {
        const parsedClientes = JSON.parse(clientesSalvos);
        // Verifique se os dados são um array, caso contrário inicialize como um array vazio
        if (Array.isArray(parsedClientes)) {
          setClientes(parsedClientes);  // Carrega os dados para o estado
        } else {
          console.error("Os dados carregados não são um array:", parsedClientes);
          setClientes([]);  // Inicializa como um array vazio caso os dados sejam inválidos
        }
      } catch (error) {
        console.error("Erro ao carregar os clientes do localStorage:", error);
        setClientes([]);  // Inicializa como um array vazio caso ocorra algum erro
      }
    } else {
      setClientes([]);  // Se não houver dados, inicializa como um array vazio
    }
  }, []);

  // Função para adicionar um cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    // Recupera os clientes existentes do localStorage
    const clientesExistentes = JSON.parse(localStorage.getItem('clientes') || '[]');

    // Adiciona o novo cliente ao array de clientes existentes
    const updatedClientes = [...clientesExistentes, novoCliente];

    // Atualiza o estado com o novo array de clientes
    setClientes(updatedClientes);

    // Salva o array atualizado no localStorage
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
