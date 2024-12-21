// src/utils/salva_component_com_expiracao.ts
import { Cliente } from 'src/types/Cliente'; // Importa a interface

// Função para salvar dados com expiração
export const salvarComExpiracao = (key: string, data: Cliente[], expirarEmMs: number): void => {
  // Normaliza os dados para garantir que campos vazios se tornem null
  const dadosNormalizados: Cliente[] = data.map(cliente => ({
    id: cliente.id || undefined,  // Mantém o ID se presente, senão undefined
    tipo_cliente: cliente.tipo_cliente || null,  // Tipo de Cliente (não pode ser vazio)
    nome_cliente: cliente.nome_cliente || null,  // Nome do Cliente
    doc_cliente: cliente.doc_cliente || null,  // Documento do Cliente (CPF/CNPJ)
    endereco_cliente: cliente.endereco_cliente || null,  // Endereço
    num_cliente: cliente.num_cliente || null,  // Número do endereço
    bairro_cliente: cliente.bairro_cliente || null,  // Bairro
    cidade_cliente: cliente.cidade_cliente || null,  // Cidade
    uf_cliente: cliente.uf_cliente || null,  // UF
    cep_cliente: cliente.cep_cliente || null,  // CEP
    telefone_cliente: cliente.telefone_cliente || null,  // Telefone
    telefone_rec_cliente: cliente.telefone_rec_cliente || null,  // Telefone de recado
    whatsapp_cliente: cliente.whatsapp_cliente || null,  // WhatsApp
    fornecedor_cliente: cliente.fornecedor_cliente || null,  // Fornecedor
    acao: cliente.acao || null,  // Ação adicional
    nome: cliente.nome || null,  // Nome extra (caso necessário)
    email: cliente.email || null,  // E-mail extra (caso necessário)
    telefone: cliente.telefone || null,  // Telefone extra (caso necessário)
    email_funcionario: cliente.email_funcionario || null,  // E-mail do responsável
    enviado: cliente.enviado,  // Status de envio (pode ser true ou false)
    data_cadastro_cliente: cliente.data_cadastro_cliente || null, // Data de cadastro
    created_at: cliente.created_at || null, // Data de criação
    updated_at: cliente.updated_at || null, // Data de atualização
    usuario_id: cliente.usuario_id || null, // Chave estrangeira para o usuário
  }));

  // Armazena os dados no localStorage com o tempo de expiração
  const expiração = Date.now() + expirarEmMs;
  localStorage.setItem(key, JSON.stringify({ dados: dadosNormalizados, expiração }));
};

// Função para carregar dados com verificação de expiração
export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number): Cliente[] | null => {
  const dados = localStorage.getItem(key);

  if (!dados) {
    console.log(`${key} não encontrado no localStorage`);
    return null;
  }

  try {
    // Verifica se os dados são um JSON válido
    const dadosComExpiracao = JSON.parse(dados);

    // Verifica se a estrutura dos dados é a esperada
    if (!dadosComExpiracao || !dadosComExpiracao.dados || !dadosComExpiracao.expiração) {
      console.error(`Formato inválido dos dados no ${key}`);
      return null;
    }

    const { dados: data, expiração } = dadosComExpiracao;

    // Verifica se os dados ainda não expiraram
    if (Date.now() < expiração) {
      return data; // Retorna os dados se não expiraram
    } else {
      console.log(`${key} expirou e foi removido.`);
      localStorage.removeItem(key); // Remove o item caso tenha expirado
      return null;
    }
  } catch (error) {
    // Se ocorrer um erro de parse, provavelmente os dados não são válidos
    console.error(`Erro ao carregar ou analisar os dados de ${key}:`, error);
    // Remover o item corrompido para evitar problemas futuros
    localStorage.removeItem(key);
    return null;
  }
};

