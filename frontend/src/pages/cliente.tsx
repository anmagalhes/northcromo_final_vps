import React, { useState } from 'react';
import { Cliente } from 'src/types';  // Importando Cliente do index.ts
import { salva_component } from '@utils/salva_component';  // Importando a função salva_component

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

    // Exibindo os dados no console antes de chamar a função de adicionar
    console.log("Cliente a ser adicionado:", novoCliente);  // Exibe o objeto de cliente no console

    // Chama a função salva_component passando o tipo do formulário
    salva_component('cliente');  // Passando 'cliente' como tipo de formulário

    // Adicionando o novo cliente
    onClienteAdicionado(novoCliente);

    setNome('');
    setEmail('');
    setTelefone('');
  };

  return (
    <form id="cliente-form" onSubmit={handleSubmit}>  {/* Adicionando o id ao formulário */}
      <input
        type="text"
        id="nome"
        className="my-input"  // Adicionando a classe
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
      />
      <input
        type="email"
        id="email"
        className="my-input"  // Adicionando a classe
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="text"
        id="telefone"
        className="my-input"  // Adicionando a classe
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => setTelefone(e.target.value)}
      />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;
