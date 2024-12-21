// src/types/Cliente.ts
export interface Cliente {
  id?: number;                   // O ID é auto-incrementado no banco de dados, por isso é opcional.
  tipo_cliente: string | null;    // Tipo de Cliente (Pessoa Física ou Jurídica, etc.)
  nome_cliente: string | null;    // Nome do Cliente
  doc_cliente: string | null;     // Documento do Cliente (CPF/CNPJ)
  endereco_cliente: string | null; // Endereço do Cliente
  num_cliente: string | null;     // Número do endereço
  bairro_cliente: string | null;  // Bairro
  cidade_cliente: string | null;  // Cidade
  uf_cliente: string | null;      // UF (Estado)
  cep_cliente: string | null;     // CEP
  telefone_cliente: string | null; // Telefone do Cliente
  telefone_rec_cliente: string | null; // Telefone de recado
  whatsapp_cliente: string | null;   // WhatsApp do Cliente
  fornecedor_cliente: string | null; // Fornecedor do Cliente
  email_funcionario: string | null;  // E-mail do funcionário responsável
  acao: string | null;           // Observações ou ação adicional sobre o cliente
  data_cadastro_cliente?: string | null; // Data de cadastro do cliente (timestamp)
  created_at?: string | null;         // Data de criação
  updated_at?: string | null;         // Data de atualização
  usuario_id?: number | null;         // Chave estrangeira para o usuário
  grupo_produto?: number | null;
  enviado?: boolean;                  // Indica se o cliente foi enviado (opcional)
  
  // Adicione os campos extra, se necessário, para atender ao seu front-end.
  nome?: string | null;    // Nome extra do cliente, caso necessário.
  email?: string | null;   // E-mail extra do cliente, caso necessário.
  telefone?: string | null; // Telefone extra do cliente, caso necessário.
}
