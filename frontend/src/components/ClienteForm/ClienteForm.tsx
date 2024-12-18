// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types';  // Importando Cliente do index.ts

interface ClienteFormProps {
  onClienteAdicionado: (cliente: Cliente) => void;
}

const ClienteForm: React.FC<ClienteFormProps> = ({ onClienteAdicionado }) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const novoCliente: Cliente = {
      id: Date.now(),
      nome,
      email,
      telefone,
    };

    onClienteAdicionado(novoCliente);
    setNome('');
    setEmail('');
    setTelefone('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => setTelefone(e.target.value)}
      />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;
