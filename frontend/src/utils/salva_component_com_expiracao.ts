// src/utils/salva_component_com_expiracao.ts
export const salvarComExpiracao = (key: string, data: any, expirarEmMs: number) => {
  const expiracao = Date.now() + expirarEmMs; // Define a expiração
  const dadosComExpiracao = {
    data,
    expiracao,
  };

  localStorage.setItem(key, JSON.stringify(dadosComExpiracao)); // Salva com expiração no localStorage
  console.log(`${key} salvo com expiração no localStorage:`, dadosComExpiracao);
};

export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number) => {
  const dados = localStorage.getItem(key);

  if (dados) {
    try {
      const dadosComExpiracao = JSON.parse(dados);
      const { data, expiracao } = dadosComExpiracao;

      if (Date.now() < expiracao) {
        return data; // Retorna os dados se não expiraram
      } else {
        console.log(`${key} expirou e foi removido.`);
        localStorage.removeItem(key); // Remove o item caso tenha expirado
      }
    } catch (error) {
      console.error(`Erro ao carregar ou analisar os dados de ${key}:`, error);
      return null;
    }
  }

  return null; // Retorna null se não houver dados ou se tiver expirado
};
