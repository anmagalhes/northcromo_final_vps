import React, { useState } from 'react';
import { Cliente } from 'src/types';  // Importando Cliente do index.ts
import { salva_component } from 'src/utils/salva_component';  // Importando a função salva_component

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

    // Chama a função salva_component, passando o tipo do formulário
    salva_component('cliente');  // Passando 'cliente' como tipo de formulário

    onClienteAdicionado(novoCliente);
    setNome('');
    setEmail('');
    setTelefone('');
  };

  // Função para exibir no console os dados digitados em tempo real
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { id, value } = e.target;
    console.log(`${id} digitado: ${value}`);
  };

  return (
    <form id="cliente-form" onSubmit={handleSubmit}>
      <input
        type="text"
        className="my-input"
        id="nome"
        placeholder="Nome"
        value={nome}
        onChange={(e) => {
          setNome(e.target.value);
          handleInputChange(e);  // Exibe os dados digitados no console em tempo real
        }}
      />
      <input
        type="email"
        className="my-input"
        id="email"
        placeholder="Email"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
          handleInputChange(e);  // Exibe os dados digitados no console em tempo real
        }}
      />
      <input
        type="text"
        className="my-input"
        id="telefone"
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => {
          setTelefone(e.target.value);
          handleInputChange(e);  // Exibe os dados digitados no console em tempo real
        }}
      />
      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;


