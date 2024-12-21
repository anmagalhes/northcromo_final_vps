// src/pages/cliente.tsx
import React, { useState, useEffect } from 'react';
import { Cliente } from '../types/Cliente'; // Tipo Cliente
import ClienteForm from '../components/ClienteForm/ClienteForm'; // Formulário de Cliente
import ClienteList from '../components/ClienteList/ClienteList'; // Lista de Clientes
import Button from '../components/Button/Button'; // Componente de Botão
import { salvarComExpiracao } from '../utils/salva_component_com_expiracao'; // Funções de expiração

// API 
import { enviarParaBackend } from '../api/clientes';
import { editarClienteNoBackend } from '../api/clientes';
import { deleteCliente } from '../api/clientes'; 

// Função para obter a data atual
const getCurrentTime = (): number => {
  return new Date().getTime();
};

const ClientePage: React.FC = () => {
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
  
      // Certifique-se de que os campos opcionais sejam enviados como null se não forem preenchidos
      novoCliente.telefone_rec_cliente = novoCliente.telefone_rec_cliente ? novoCliente.telefone_rec_cliente : null;
      novoCliente.whatsapp_cliente = novoCliente.whatsapp_cliente ? novoCliente.whatsapp_cliente : null;
      novoCliente.email_funcionario = novoCliente.email_funcionario ? novoCliente.email_funcionario : null;
      novoCliente.acao = novoCliente.acao ? novoCliente.acao : null;
  
      // Garantir que os campos obrigatórios sejam preenchidos
      novoCliente.nome_cliente = novoCliente.nome_cliente || null;
      novoCliente.email_funcionario = novoCliente.email_funcionario || '';  // Atribuindo string vazia caso seja null;
      novoCliente.telefone_cliente = novoCliente.telefone_cliente || null;
  
      // Envia o cliente para o backend
      const response = await enviarParaBackend(novoCliente);
  
      // Se a resposta do backend for bem-sucedida, marca o cliente como enviado
      if (response && response.success) {
        novoCliente.enviado = true;
        // Atualiza a lista de clientes com a marcação de enviado
        adicionarClienteAoLocalStorage(novoCliente);
      } else {
        console.error("Falha ao enviar cliente para o backend", response?.message || "Resposta inválida");
      }
    } catch (error) {
      console.error("Erro ao adicionar cliente:", error);
    }
  };
  
  // Função para editar um clientes
  const handleEditCliente = async (clienteEditado: Cliente) => {
    try {
      if (clienteEditado.id !== undefined) {
        // Envia os dados do cliente editado para o backend
        const response = await editarClienteNoBackend(clienteEditado.id, clienteEditado);

        if (response && response.success) {
          // Atualiza a lista de clientes no estado com os dados modificados
          const updatedClientes = clientes.map((cliente) =>
            cliente.id === clienteEditado.id ? clienteEditado : cliente
          );
          setClientes(updatedClientes);  // Atualiza o estado com a lista de clientes

          // Atualiza o localStorage com os clientes modificados (com expiração)
          salvarComExpiracao('clientes', updatedClientes, 24 * 60 * 60 * 1000);  // Salvando com expiração de 24 horas
        } else {
          console.error("Erro ao editar cliente no backend:", response?.message || "Resposta inválida");
        }
      } else {
        console.error("ID do cliente não encontrado");
      }
    } catch (error) {
      console.error("Erro ao editar cliente:", error);
    }
  };

  // Função para excluir um cliente
  const handleDeleteCliente = async (id: number) => {
    try {
      // Envia a requisição para excluir o cliente no backend
      const response = await deleteCliente(id);

      if (response && response.success) {
        // Se a exclusão for bem-sucedida, remove o cliente da lista no estado
        const updatedClientes = clientes.filter((cliente) => cliente.id !== id);
        setClientes(updatedClientes);  // Atualiza o estado com a lista de clientes

        // Salva o array atualizado no localStorage com expiração de 24 horas
        salvarComExpiracao('clientes', updatedClientes, 24 * 60 * 60 * 1000);  // Salvando com expiração de 24 horas
      } else {
        console.error("Erro ao excluir cliente no backend:", response?.message || "Resposta inválida");
      }
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
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} onEdit={handleEditCliente} />

      {/* Botão de ação */}
      <Button label="Clique aqui" onClick={() => alert('Ação de botão executada!')} />
    </div>
  );
};

export default ClientePage;

