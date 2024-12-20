// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from '../types/Cliente'; // Tipo Cliente
import ClienteForm from '../components/ClienteForm/ClienteForm'; // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList'; // Lista de Clientes
import Button from '../components/Button/Button'; // Componente de Botão
import { salvarComExpiracao } from '../utils/salva_component_com_expiracao'; // Funções de expiração

// API 
import { enviarParaBackend } from '../api/clientes';

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
        let clientesCarregados: Cliente[] = [];
  
        try {
          // Tenta parsear o conteúdo do localStorage
          clientesCarregados = JSON.parse(clientesCarregadosStr);
  
          // Verifica se o resultado é um array de objetos Cliente válidos
          if (
            !Array.isArray(clientesCarregados) || 
            !clientesCarregados.every((item: any) => item.id && item.nome && item.email && item.telefone)
          ) {
            throw new Error("Dados inválidos no localStorage");
          }
        } catch (error) {
          console.error("Erro ao parsear clientes do localStorage", error);
          clientesCarregados = []; // Retorna um array vazio em caso de erro
        }
  
        return clientesCarregados;
      }
  
      return []; // Retorna um array vazio caso não haja dados no localStorage
    } catch (error) {
      console.error("Erro ao carregar os dados do localStorage", error);
      return []; // Retorna um array vazio em caso de erro
    }
  };
  
  // Função para adicionar um cliente ao localStorage
  const adicionarClienteAoLocalStorage = (novoCliente: Cliente) => {
    try {
      // Recupera os clientes existentes do localStorage (se houver)
      const clientesExistentesStr = localStorage.getItem('clientes');
      let clientesExistentes: Cliente[] = [];
  
      // Se existirem clientes no localStorage, tente parsear
      if (clientesExistentesStr) {
        try {
          clientesExistentes = JSON.parse(clientesExistentesStr);
  
          // Verifica se a estrutura é um array válido
          if (!Array.isArray(clientesExistentes)) {
            console.warn("Dados no localStorage não são um array, inicializando com array vazio.");
            clientesExistentes = [];
          }
        } catch (error) {
          console.error("Erro ao parsear clientes do localStorage", error);
          clientesExistentes = [];
        }
      }
  
      // Adiciona o novo cliente ao array
      const updatedClientes = [...clientesExistentes, novoCliente];
  
      // Atualiza o localStorage com o novo array de clientes
      localStorage.setItem('clientes', JSON.stringify(updatedClientes));
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
  const handleClienteAdicionado = async (novoCliente: Cliente) => {
    try {
      // Marca o cliente como "não enviado" inicialmente
      novoCliente.enviado = false;
  
      // Adiciona o cliente ao localStorage
      adicionarClienteAoLocalStorage(novoCliente);
  
      // Envia os dados para o backend
      const response = await enviarParaBackend(novoCliente);
   
      // Se a resposta do backend for bem-sucedida, marca o cliente como enviado
      if (response.success) {
        novoCliente.enviado = true;
        // Atualiza o localStorage com a marcação de enviado
        adicionarClienteAoLocalStorage(novoCliente);
      } else {
        console.error("Falha ao enviar cliente para o backend");
      }
    } catch (error) {
      console.error("Erro ao adicionar cliente:", error);
    }
  };
  
  // Função para excluir um cliente Analisar
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
