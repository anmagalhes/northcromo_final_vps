// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';  // Certifique-se de que o tipo Cliente está correto
import { salva_component } from 'src/utils';  // Certifique-se de que o tipo Cliente está correto

interface ClienteFormProps {
  onClienteAdicionado: (cliente: Cliente) => void;  // Definindo o tipo da prop
}

const ClienteForm: React.FC<ClienteFormProps> = ({ onClienteAdicionado }) => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const novoCliente: Cliente = {
      id: Date.now(),  // Você pode gerar o ID de forma diferente dependendo do seu backend
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
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        id="nome"  // Definindo o ID para cada input
        className="my-input"  // Adicionando a classe 'my-input' para selecionar os inputs na função salva_component
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="email"
        id="email"  // Definindo o ID para cada input
        className="my-input"  // Adicionando a classe 'my-input' para selecionar os inputs na função salva_component
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        id="telefone"  // Definindo o ID para cada input
        className="my-input"  // Adicionando a classe 'my-input' para selecionar os inputs na função salva_component
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => setTelefone(e.target.value)}
      />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;
