// src/components/ClienteList/ClienteList.tsx
import React from 'react';

// Interface para o tipo de dados dos clientes
interface Cliente {
  id: number;
  nome: string;
  email: string;
  telefone: string;
}

// Definindo os props que o componente espera
interface ClienteListProps {
  clientes: Cliente[];
}

const ClienteList: React.FC<ClienteListProps> = ({ clientes }) => {
  return (
    <div>
      <h2>Lista de Clientes</h2>
      {clientes.length === 0 ? (
        <p>Não há clientes cadastrados.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Nome</th>
              <th>Email</th>
              <th>Telefone</th>
            </tr>
          </thead>
          <tbody>
            {clientes.map((cliente) => (
              <tr key={cliente.id}>
                <td>{cliente.id}</td>
                <td>{cliente.nome}</td>
                <td>{cliente.email}</td>
                <td>{cliente.telefone}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ClienteList;

