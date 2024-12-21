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
      tipo_cliente: null, // Se não for necessário, mantenha null
      nome_cliente: nome || null, // Se o campo estiver vazio, atribui null
      doc_cliente: null, // Adicione conforme necessário
      endereco_cliente: null, // Adicione conforme necessário
      num_cliente: null, // Adicione conforme necessário
      bairro_cliente: null, // Adicione conforme necessário
      cidade_cliente: null, // Adicione conforme necessário
      uf_cliente: null, // Adicione conforme necessário
      cep_cliente: null, // Adicione conforme necessário
      telefone_cliente: telefone || null, // Se o campo estiver vazio, atribui null
      telefone_rec_cliente: null, // Adicione conforme necessário
      whatsapp_cliente: null, // Adicione conforme necessário
      fornecedor_cliente: null, // Adicione conforme necessário
      email_funcionario: email || null, // Se o campo estiver vazio, atribui null
      acao: null, // Adicione conforme necessário
      nome: nome || null, // Se nome estiver vazio, salva como null
      email: email || null, // Se email estiver vazio, salva como null
      telefone: telefone || null, // Se telefone estiver vazio, salva como null
      enviado: false, // Valor inicial de "enviado" como false
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
        id="nome_cliente"
        className="my-input"
        placeholder="Nome"
        value={nome}
        onChange={(e) => setNome(e.target.value)}  // Atualiza o estado 'nome'
      />

      <input
        type="email"
        id="email_funcionario"
        className="my-input"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}  // Atualiza o estado 'email'
      />

      <input
        type="text"
        id="telefone_cliente"
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
