// src/components/ClienteList/ClienteList.tsx
import React from 'react';
import { Cliente } from 'src/types/Cliente'; // Importando o tipo Cliente

// Definindo o tipo das props do componente ClienteList
interface ClienteListProps {
  clientes: Cliente[];  // Array de clientes, que será passado como prop
  onDelete: (id: number) => void;  // Função para excluir cliente, passada como prop
  onEdit: (clienteEditado: Cliente) => void;  // Função para editar cliente, passada como prop
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes, onDelete, onEdit }) => {
  return (
    <div>
      <h2>Lista de Clientes</h2>
      <ul>
        {clientes.length > 0 ? (
          // Renderizando a lista de clientes
          clientes.map(cliente => (
            <li key={cliente.id}>
              {cliente.nome} - {cliente.email} - {cliente.telefone}
              <button onClick={() => onEdit(cliente)}>Editar</button>  {/* Chamando a função onEdit */}
              <button onClick={() => onDelete(cliente.id)}>Excluir</button> {/* Chamando a função onDelete */}
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
