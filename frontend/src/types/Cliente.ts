export interface Cliente {
  id?: number;  // Pode ser opcional, pois o ID é gerado automaticamente pelo banco
  tipo_cliente: string | null;  // Pode ser null
  nome_cliente: string | null;  // Pode ser null
  doc_cliente: string | null;  // Pode ser null
  endereco_cliente: string | null;  // Pode ser null
  num_cliente: string | null;  // Pode ser null
  bairro_cliente: string | null;  // Pode ser null
  cidade_cliente: string | null;  // Pode ser null
  uf_cliente: string | null;  // Pode ser null
  cep_cliente: string | null;  // Pode ser null
  telefone_cliente: string | null;  // Pode ser null
  telefone_rec_cliente?: string | null;  // Pode ser null ou não definido
  whatsapp_cliente?: string | null;  // Pode ser null ou não definido
  fornecedor_cliente: string | null;  // Pode ser null
  email_funcionario?: string | null;  // Pode ser null ou não definido
  acao?: string | null;  // Pode ser null ou não definido
  enviado?: boolean;  // Pode ser opcional (controle de envio)
}

