// src/utils/salva_component_com_expiracao.ts
export const salvarComExpiracao = (key: string, data: any, expirarEmMs: number) => {
  const expiracao = Date.now() + expirarEmMs; // Calcula o timestamp de expiração
  const dadosComExpiracao = {
    data,
    expiracao,  // Adiciona a expiração
  };

  try {
    // Serializa o objeto e armazena no localStorage
    localStorage.setItem(key, JSON.stringify(dadosComExpiracao));
    console.log(`${key} salvo com expiração no localStorage:`, dadosComExpiracao);
  } catch (error) {
    console.error(`Erro ao salvar dados de ${key} no localStorage:`, error);
  }
};


export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number) => {
  const dados = localStorage.getItem(key);

  if (!dados) {
    console.log(`${key} não encontrado no localStorage`);
    return null;
  }

  try {
    const dadosComExpiracao = JSON.parse(dados);

    // Verifica se a estrutura está correta
    if (!dadosComExpiracao.data || !dadosComExpiracao.expiracao) {
      console.error(`Formato inválido dos dados no ${key}`);
      return null;
    }

    const { data, expiracao } = dadosComExpiracao;

    if (Date.now() < expiracao) {
      return data;  // Retorna os dados se não expiraram
    } else {
      console.log(`${key} expirou e foi removido.`);
      localStorage.removeItem(key); // Remove o item caso tenha expirado
      return null;
    }
  } catch (error) {
    console.error(`Erro ao carregar ou analisar os dados de ${key}:`, error);
    return null;
  }
};
