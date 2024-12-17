// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';

interface ClienteFormProps {
  onClienteAdicionado: (cliente: Cliente) => void; // Prop para enviar o cliente adicionado
}

const ClienteForm: React.FC<ClienteFormProps> = ({ onClienteAdicionado }) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');

  // Função para lidar com a submissão do formulário
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const novoCliente: Cliente = {
      id: Date.now(), // Usando timestamp para id único
      nome,
      email,
      telefone,
    };

    onClienteAdicionado(novoCliente); // Chamando a função passada por props para adicionar o cliente
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
