// src/components/ClienteList/ClienteList.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Cliente } from 'src/types/Cliente';  // Certifique-se de importar o tipo corretamente

interface ClienteListProps {
  clientes: Cliente[];  // Usando o tipo correto para o array de clientes
  onDelete: (id: number) => void;  // Função para excluir cliente
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes, onDelete }) => {
  const [clientesState, setClientesState] = useState<Cliente[]>(clientes);  // Inicia com a lista passada como props

  // Carregar clientes do backend ao montar o componente
  useEffect(() => {
    // Se clientes estiver vazio (ex.: ao montar), fazer a requisição
    if (clientesState.length === 0) {
      axios.get('https://northcromocontrole.com.br/api/cliente')  // URL da API para buscar os clientes
        .then(response => {
          setClientesState(response.data);  // Atualiza o estado com os dados recebidos
        })
        .catch(error => {
          console.error('Erro ao buscar clientes:', error);
        });
    }
  }, [clientesState.length]);  // A dependência garante que a requisição seja feita uma vez

  // Função para excluir cliente
  const handleDelete = (id: number) => {
    axios.delete(`https://northcromocontrole.com.br/api/cliente/${id}`)  // Excluindo cliente via API
      .then(() => {
        setClientesState((prevState) => prevState.filter(cliente => cliente.id !== id));  // Atualiza o estado removendo o cliente
      })
      .catch((error) => {
        console.error('Erro ao excluir cliente:', error);
      });
  };

  return (
    <div>
      <h2>Lista de Clientes</h2>
      <ul>
        {clientesState.length === 0 ? (
          <p>Não há clientes cadastrados.</p>
        ) : (
          clientesState.map((cliente) => (
            <li key={cliente.id}>
              {cliente.nome} - {cliente.email} - {cliente.telefone}
              <button onClick={() => handleDelete(cliente.id)}>Excluir</button>
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default ClienteList;

