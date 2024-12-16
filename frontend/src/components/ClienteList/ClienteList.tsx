// src/components/ClienteList/ClienteList.tsx
import React from 'react';
import { Cliente } from '../../types/Cliente';  // Certifique-se de importar corretamente

interface ClienteListProps {
  clientes: Cliente[];  // Usando o tipo correto para o array de clientes
  onDelete: (id: number) => void;
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes, onDelete }) => {
  return (
    <div>
      <ul>
        {clientes.map(cliente => (
          <li key={cliente.id}>
            {cliente.nome} - {cliente.email} - {cliente.telefone}
            <button onClick={() => onDelete(cliente.id)}>Excluir</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ClienteList;
