// src/components/ClienteForm/ClienteForm.tsx
import React, { useState } from 'react';
import { Cliente } from 'src/types/Cliente';
import { salva_component } from '@utils/salva_component';

interface ClienteFormProps {
  onClienteAdicionado: (cliente: Cliente) => void; // Função passada via props para adicionar o cliente
}

const ClienteForm: React.FC<ClienteFormProps> = ({ onClienteAdicionado }) => {
  const [nome, setNome] = useState<string>(''); // Estado para nome
  const [email, setEmail] = useState<string>(''); // Estado para email
  const [telefone, setTelefone] = useState<string>(''); // Estado para telefone

  // Função chamada no envio do formulário
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Instanciando o novo cliente com base nos dados do formulário
    const novoCliente: Cliente = {
      id: Date.now(), // ID único gerado com base no timestamp
      nome: nome || '', // Se o campo estiver vazio, atribui uma string vazia
      email: email || '', // O mesmo para o email
      telefone: telefone || '', // E o mesmo para o telefone
    };

    // Chama a função passada via props para adicionar o cliente no componente pai
    onClienteAdicionado(novoCliente);

    // Salva o novo cliente no localStorage
    salva_component('clientes', novoCliente);

    // Limpa os campos após o envio
    setNome('');
    setEmail('');
    setTelefone('');
  };

  return (
    <form id="clientes-form" onSubmit={handleSubmit}>
      <input
        type="text"
        id="nome"
        className="my-input"
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}  // Atualiza o estado 'nome'
      />

      <input
        type="email"
        id="email"
        className="my-input"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}  // Atualiza o estado 'email'
      />

      <input
        type="text"
        id="telefone"
        className="my-input"
        placeholder="Telefone"
        value={telefone}
        onChange={(e) => setTelefone(e.target.value)}  // Atualiza o estado 'telefone'
      />

      <button type="submit">Adicionar Cliente</button>
    </form>
  );
};

export default ClienteForm;