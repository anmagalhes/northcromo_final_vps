// Função para salvar dados com expiração
export const salvarComExpiracao = (key: string, data: any, expirarEmMs: number) => {
  const expiracao = Date.now() + expirarEmMs; // Calcula a data de expiração
  const dadosComExpiracao = {
    data,
    expiracao,
  };

  try {
    // Salva no localStorage
    localStorage.setItem(key, JSON.stringify(dadosComExpiracao));
    console.log(`${key} salvo com expiração no localStorage:`, dadosComExpiracao);
  } catch (error) {
    console.error(`Erro ao salvar dados de ${key} no localStorage:`, error);
  }
};

// Função para carregar dados com verificação de expiração
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