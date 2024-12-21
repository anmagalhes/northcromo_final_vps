// src/types/Cliente.ts
export interface Cliente {
  id?: number;
  tipo_cliente: string | null;
  nome_cliente: string | null;
  doc_cliente: string | null;
  endereco_cliente: string | null;
  num_cliente: string | null;
  bairro_cliente: string | null;
  cidade_cliente: string | null;
  uf_cliente: string | null;
  cep_cliente: string | null;
  telefone_cliente: string | null;
  telefone_rec_cliente: string | null;
  whatsapp_cliente: string | null;
  fornecedor_cliente: string | null;
  email_funcionario: string | null;
  acao: string | null;
  nome: string | null;  // O nome do cliente (provavelmente você quer ter isso também)
  email: string | null;
  telefone: string | null;
  enviado?: boolean;
}
