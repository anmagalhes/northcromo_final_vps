// src/utils/salva_component_com_expiracao.ts

// Função para salvar com data de expiração
export const salvarComExpiracao = (chave: string, dados: any, duracao: number) => {
    const dadosComData = {
      dados,
      timestamp: new Date().getTime(), // Marca o tempo atual em milissegundos
    };
    localStorage.setItem(chave, JSON.stringify(dadosComData));
    console.log(`${chave} salvo no localStorage com expiração de ${duracao} ms`);
  };
  
  // Função para carregar com verificação de expiração
  export const carregarComVerificacaoDeExpiracao = (chave: string, duracao: number) => {
    const dadosArmazenados = localStorage.getItem(chave);
  
    if (!dadosArmazenados) return null; // Não há dados armazenados
  
    const { dados, timestamp } = JSON.parse(dadosArmazenados);
  
    // Verifica se os dados expiraram
    const expiracao = new Date().getTime() - timestamp;
    if (expiracao > duracao) {
      localStorage.removeItem(chave); // Dados expiraram, remove do localStorage
      console.log(`${chave} expirado e removido do localStorage.`);
      return null;
    }
  
    return dados;
  };
  