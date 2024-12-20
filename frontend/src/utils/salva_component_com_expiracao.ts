// Função para salvar dados no localStorage com expiração
export const salvarComExpiracao = (key: string, data: any, expirarEmMs: number) => {
  try {
    const expiracao = Date.now() + expirarEmMs; // Define o tempo de expiração
    const dadosComExpiracao = {
      data,
      expiracao,
    };

    localStorage.setItem(key, JSON.stringify(dadosComExpiracao)); // Salva no localStorage
    console.log(`${key} salvo com expiração no localStorage:`, dadosComExpiracao);
  } catch (error) {
    console.error(`Erro ao salvar dados com expiração para a chave ${key}:`, error);
  }
};

// Função para carregar dados do localStorage verificando a expiração
export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number) => {
  try {
    const dados = localStorage.getItem(key);  // Busca os dados no localStorage

    if (dados) {
      const dadosComExpiracao = JSON.parse(dados);  // Parseia os dados JSON
      const { data, expiracao } = dadosComExpiracao;

      if (Date.now() < expiracao) {
        console.log(`Dados para ${key} carregados com sucesso e não expiraram.`);
        return data; // Retorna os dados se não expiraram
      } else {
        console.log(`${key} expirou e foi removido.`);
        localStorage.removeItem(key); // Remove se expirou
      }
    }

    return null; // Retorna null se não houver dados ou se expiraram
  } catch (error) {
    console.error(`Erro ao carregar ou analisar os dados de ${key}:`, error);
    return null; // Retorna null se ocorrer um erro ao carregar os dados
  }
};
