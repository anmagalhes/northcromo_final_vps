// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from '../types/Cliente'; // Tipo Cliente
import ClienteForm from '../components/ClienteForm/ClienteForm'; // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList'; // Lista de Clientes
import Button from '../components/Button/Button'; // Componente de Botão
import { salvarComExpiracao, carregarComVerificacaoDeExpiracao } from '../utils/salva_component_com_expiracao'; // Funções de expiração

const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Estado para armazenar a lista de clientes
//
  // Carregar os clientes do localStorage com expiração de 24 horas
  useEffect(() => {
    try {
      // Carrega os dados dos clientes e verifica a expiração (24h)
      const clientesCarregados = carregarComVerificacaoDeExpiracao('clientes', 24 * 60 * 60 * 1000); // 24 horas em ms
  
      if (clientesCarregados) {
        // Se for um único cliente, envolva em um array
        setClientes([clientesCarregados]);  // Agora setClientes recebe um array de Cliente[]
      } else {
        setClientes([]);  // Caso não haja dados ou os dados estejam expirados
      }
    } catch (error) {
      console.error("Erro ao carregar os clientes do localStorage:", error);
      setClientes([]);  // Em caso de erro, inicializa como um array vazio
    }
  }, []);  // O useEffect será executado uma única vez no carregamento da página
  
  
  // Função para adicionar um cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    try {
      // Recupera os clientes existentes do localStorage
      const clientesExistentes = JSON.parse(localStorage.getItem('clientes') || '[]');

      // Adiciona o novo cliente ao array de clientes existentes
      const updatedClientes = [...clientesExistentes, novoCliente];

      // Atualiza o estado com o novo array de clientes
      setClientes(updatedClientes);

      // Salva o array atualizado no localStorage com expiração (24h)
      salvarComExpiracao('clientes', updatedClientes, 24 * 60 * 60 * 1000);  // Salvando com expiração de 24 horas
    } catch (error) {
      console.error("Erro ao adicionar cliente ao localStorage:", error);
    }
  };

  // Função para excluir um cliente
  const handleDeleteCliente = (id: number) => {
    try {
      // Filtra o cliente a ser excluído
      const updatedClientes = clientes.filter((cliente) => cliente.id !== id);
      setClientes(updatedClientes);  // Atualiza a lista de clientes no estado

      // Salva o array atualizado no localStorage com expiração (24h)
      salvarComExpiracao('clientes', updatedClientes, 24 * 60 * 60 * 1000);  // Salvando com expiração de 24 horas
    } catch (error) {
      console.error("Erro ao excluir cliente:", error);
    }
  };

  return (
    <div>
      <h2>Gestão de Clientes</h2>

      {/* Formulário para adicionar um novo cliente */}
      <ClienteForm onClienteAdicionado={handleClienteAdicionado} />

      {/* Lista de Clientes */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />

      {/* Botão de ação */}
      <Button label="Clique aqui" onClick={() => alert('Ação de botão executada!')} />
    </div>
  );
};

export default Cliente;