// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';
import { salva_component } from '@utils/salva_component';


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

    // Chama a função onClienteAdicionado passando o novo cliente
    onClienteAdicionado(novoCliente);

    // Limpa os campos do formulário após o envio
    setNome('');
    setEmail('');
    setTelefone('');

    // Chama a função salva_component passando o nome do formulário correto ('clientes')
    salva_component('clientes', novoCliente);  // Usar 'clientes' aqui
  };

  return (
    <form id="clientes-form" onSubmit={handleSubmit}> {/* Certifique-se de que o ID seja 'clientes-form' */}
      <input
        type="text"
        id="nome"
        className="my-input"
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="email"
        id="email"
        className="my-input"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        id="telefone"
        className="my-input"
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => setTelefone(e.target.value)}
      />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;