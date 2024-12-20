// Função para salvar dados no localStorage com expiração
export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number) => {
  try {
    const dados = localStorage.getItem(key);  // Busca os dados no localStorage

    if (dados) {
      // Tente analisar os dados, mas se falhar, mostre o erro e retorne null
      let dadosComExpiracao;
      try {
        dadosComExpiracao = JSON.parse(dados);
      } catch (error) {
        console.error(`Erro ao analisar os dados de ${key}:`, error);
        return null;
      }

      const { data, expiracao } = dadosComExpiracao;

      // Verifique a expiração
      if (Date.now() < expiracao) {
        console.log(`Dados para ${key} carregados com sucesso e não expiraram.`);
        return data;  // Retorna os dados se não expiraram
      } else {
        console.log(`${key} expirou e foi removido.`);
        localStorage.removeItem(key);  // Remove o item do localStorage
      }
    }

    return null;  // Retorna null se não houver dados ou se tiver expirado
  } catch (error) {
    console.error(`Erro ao carregar ou verificar os dados de ${key}:`, error);
    return null;  // Retorna null se ocorrer um erro
  }
};
