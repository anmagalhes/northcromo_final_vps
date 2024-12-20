// src/components/ClienteList/ClienteList.tsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Cliente } from 'src/types/Cliente'; // Importando o tipo Cliente

// Definindo o tipo das props do componente ClienteList
interface ClienteListProps {
  clientes: Cliente[];  // Array de clientes, que será passado como prop
  onDelete: (id: number) => void;  // Função para excluir cliente, passada como prop
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes, onDelete }) => {
  const [clientesState, setClientesState] = useState<Cliente[]>([]);  // Estado interno para armazenar clientes

  // Carregar a lista de clientes da API quando o componente for montado
  useEffect(() => {
    // Chamando a API para buscar os dados dos clientes
    axios.get('https://northcromocontrole.com.br/api/cliente') // Endpoint para pegar os dados dos clientes
      .then((response) => {
        setClientesState(response.data);  // Atualizando o estado com os dados recebidos
      })
      .catch((error) => {
        console.error('Erro ao buscar clientes:', error);  // Tratando erro na requisição
      });
  }, []);  // O array vazio garante que a requisição aconteça apenas uma vez

  return (
    <div>
      <h2>Lista de Clientes</h2>
      <ul>
        {clientesState.length > 0 ? (
          // Renderizando a lista de clientes
          clientesState.map(cliente => (
            <li key={cliente.id}>
              {cliente.nome} - {cliente.email} - {cliente.telefone}
              <button onClick={() => cliente.id !== undefined && onDelete(cliente.id)}>Excluir</button>
            </li>
          ))
        ) : (
          <p>Não há clientes cadastrados.</p>  // Caso não haja clientes
        )}
      </ul>
    </div>
  );
};

export default ClienteList;
