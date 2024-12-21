// src/utils/salva_component_com_expiracao.ts
import { Cliente } from 'src/types/Cliente'; // Importa a interface

// Função para salvar dados com expiração
// Função para salvar dados com expiração
export const salvarComExpiracao = (key: string, data: Cliente[], expirarEmMs: number): void => {
  // Normaliza os dados para garantir que campos vazios se tornem null e id seja sempre um número
  const dadosNormalizados: Cliente[] = data.map(cliente => ({
    nome_cliente: cliente.nome_cliente || null,  // Se nome estiver vazio, salva como null
    email_funcionario: cliente.email_funcionario || null,  // Se email estiver vazio, salva como null
    telefone_cliente: cliente.telefone_cliente || null,  // Se telefone estiver vazio, salva como null
    id: cliente.id ?? 0,  // Substitui undefined por 0 ou outro valor padrão
    tipo_cliente: cliente.tipo_cliente || null,
    doc_cliente: cliente.doc_cliente || null,
    endereco_cliente: cliente.endereco_cliente || null,
    num_cliente: cliente.num_cliente || null,
    bairro_cliente: cliente.bairro_cliente || null,
    cidade_cliente: cliente.cidade_cliente || null,
    uf_cliente: cliente.uf_cliente || null,
    cep_cliente: cliente.cep_cliente || null,
    telefone_rec_cliente: cliente.telefone_rec_cliente || null,
    whatsapp_cliente: cliente.whatsapp_cliente || null,
    fornecedor_cliente: cliente.fornecedor_cliente || null,
    acao: cliente.acao || null,
    nome: cliente.nome || null,  // Se nome estiver vazio, salva como null
    email: cliente.email || null,  // Se email estiver vazio, salva como null
    telefone: cliente.telefone || null,  // Se telefone estiver vazio, salva como null
    enviado: cliente.enviado,  // Mantém o valor de "enviado"
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

