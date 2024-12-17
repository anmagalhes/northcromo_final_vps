// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';  // Garantindo o tipo correto

// Tipo de props
interface ClienteFormProps {
  onClienteAdicionado: (cliente: Cliente) => void; // Espera um tipo 'Cliente'
}

const ClienteForm: React.FC<ClienteFormProps> = ({ onClienteAdicionado }) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Garantindo que o novo cliente tenha o tipo 'Cliente'
    const novoCliente: Cliente = {
      id: Date.now(),
      nome,
      email,
      telefone,
    };

    onClienteAdicionado(novoCliente); // Passando o cliente com o tipo correto
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
