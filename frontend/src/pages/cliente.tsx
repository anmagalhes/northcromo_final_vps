import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ClienteList from '../../components/ClienteList/ClienteList';  // Ajuste o caminho conforme necessário
import { Cliente } from '../../types/Cliente';

const ClientePage: React.FC = () => {
  const [clientes, setClientes] = useState<Cliente[]>([]);  // Estado para armazenar a lista de clientes

  useEffect(() => {
    // Requisição GET para buscar os clientes do backend Flask
    axios.get('http://localhost:5000/api/clientes')  // Ajuste a URL conforme necessário
      .then(response => {
        setClientes(response.data);  // Atualiza o estado com a resposta da API
      })
      .catch(error => {
        console.error('Erro ao buscar clientes:', error);  // Tratar erro caso falhe
      });
  }, []);  // O array vazio garante que a requisição seja feita apenas uma vez ao carregar o componente

  // Função para excluir um cliente
  const handleDeleteCliente = async (id: number) => {
    try {
      await axios.delete(`http://localhost:5000/api/clientes/${id}`);  // Requisição DELETE para excluir o cliente
      setClientes(clientes.filter(cliente => cliente.id !== id));  // Atualiza o estado removendo o cliente excluído
    } catch (error) {
      console.error('Erro ao excluir cliente:', error);  // Tratar erro caso falhe
    }
  };

  return (
    <div>
      <h1>Lista de Clientes</h1>
      {/* Passando as propriedades para o ClienteList */}
      <ClienteList clientes={clientes} onDelete={handleDeleteCliente} />
    </div>
  );
};

export default ClientePage;
