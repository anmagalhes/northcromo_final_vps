// src/utils/salva_component_com_expiracao.ts
import { Cliente }from 'src/types/Cliente'; // Importa a interface

// Função para salvar dados com expiração
export const salvarComExpiracao = (key: string, data: Cliente[], expirarEmMs: number): void => {
  // Normaliza os dados para garantir que campos vazios se tornem null
  const dadosNormalizados: Cliente[] = data.map(cliente => ({
    nome: cliente.nome || null,  // Se nome estiver vazio, salva como null
    email: cliente.email || null,  // Se email estiver vazio, salva como null
    telefone: cliente.telefone || null,  // Se telefone estiver vazio, salva como null
    id: cliente.id  // Mantém o ID
  }));

  // Armazena os dados no localStorage com o tempo de expiração
  const expiração = Date.now() + expirarEmMs;
  localStorage.setItem(key, JSON.stringify({ dados: dadosNormalizados, expiração }));
};

// Função para carregar dados com verificação de expiração
export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number): Cliente | null => {
  const dados = localStorage.getItem(key);

  if (!dados) {
    console.log(`${key} não encontrado no localStorage`);
    return null;
  }

  try {
    // Verifica se os dados são um JSON válido
    const dadosComExpiracao = JSON.parse(dados);

    // Verifique se a estrutura dos dados é a esperada
    if (!dadosComExpiracao || !dadosComExpiracao.data || !dadosComExpiracao.expiracao) {
      console.error(`Formato inválido dos dados no ${key}`);
      return null;
    }

    const { data, expiracao } = dadosComExpiracao;

    // Verifica se os dados ainda não expiraram
    if (Date.now() < expiracao) {
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
//#