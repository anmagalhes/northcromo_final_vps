// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from '../types/Cliente'; // Tipo Cliente
import ClienteForm from '../components/ClienteForm/ClienteForm'; // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList'; // Lista de Clientes
import Button from '../components/Button/Button'; // Componente de Botão
import { salvarComExpiracao } from '../utils/salva_component_com_expiracao'; // Funções de expiração

// Função para obter a data atual
const getCurrentTime = (): number => {
  return new Date().getTime();
};

const Cliente: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Estado para armazenar a lista de clientes

  // Função para carregar os clientes do localStorage com verificação de expiração
  const carregarClientes = (): Cliente[] => {
    try {
      const clientesCarregadosStr = localStorage.getItem('clientes');
      console.log("clientes carregados:", clientesCarregadosStr); // Verifique aqui
      if (clientesCarregadosStr) {
        const clientesCarregados = JSON.parse(clientesCarregadosStr);
        console.log("clientes após parse:", clientesCarregados); // Verifique após parse
        if (Array.isArray(clientesCarregados) && clientesCarregados.every((item: any) => item.id && item.nome && item.email && item.telefone)) {
          return clientesCarregados;
        } else {
          console.warn("Dados inválidos no localStorage.");
          return [];
        }
      }
      return [];
    } catch (error) {
      console.error("Erro ao carregar os dados do localStorage", error);
      return [];
    }
  };
  
        // Verifica se os dados são um array de clientes válidos
        if (Array.isArray(clientesCarregados) && clientesCarregados.every((item: any) => item.id && item.nome && item.email && item.telefone)) {
          return clientesCarregados;
        } else {
          console.warn("Dados inválidos no localStorage. Retornando lista vazia.");
          return [];
        }
      }
      return [];
    } catch (error) {
      console.error("Erro ao carregar os dados do localStorage", error);
      return [];
    }
  };

  // Função para adicionar um cliente ao localStorage
  const adicionarClienteAoLocalStorage = (novoCliente: Cliente) => {
    try {
      const clientesExistentesStr = localStorage.getItem('clientes');
      const clientesExistentes = clientesExistentesStr ? JSON.parse(clientesExistentesStr) : [];

      const updatedClientes = [...clientesExistentes, novoCliente];

      // Define a data de expiração para 24h a partir de agora
      const expiração = getCurrentTime() + 24 * 60 * 60 * 1000;

      localStorage.setItem('clientes', JSON.stringify(updatedClientes));
      localStorage.setItem('clientes_expiracao', expiração.toString());
    } catch (error) {
      console.error("Erro ao adicionar cliente ao localStorage:", error);
    }
  };

  // Carregar os clientes do localStorage com expiração de 24 horas
  useEffect(() => {
    const clientesCarregados = carregarClientes();  // Recupera os clientes do localStorage

    if (clientesCarregados.length > 0) {
      setClientes(clientesCarregados);  // Carrega os dados para o estado
    } else {
      setClientes([]);  // Caso não haja dados ou os dados estejam expirados
    }
  }, []);  // O useEffect será executado uma única vez no carregamento da página

  // Função para adicionar um cliente
  const handleClienteAdicionado = (novoCliente: Cliente) => {
    try {
      // Adiciona o novo cliente ao localStorage
      adicionarClienteAoLocalStorage(novoCliente);

      // Atualiza o estado com o novo array de clientes
      setClientes((prevClientes) => [...prevClientes, novoCliente]);
    } catch (error) {
      console.error("Erro ao adicionar cliente:", error);
    }
  };

  // Função para excluir um cliente
  const handleDeleteCliente = (id: number) => {
    try {
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
