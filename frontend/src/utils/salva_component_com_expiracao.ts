// src/utils/salva_component_com_expiracao.ts
// src/utils/salva_component_com_expiracao.ts
export const carregarComVerificacaoDeExpiracao = (key: string, tempoExpiracao: number): any | null => {
  try {
    const dadosString = localStorage.getItem(key);
    if (!dadosString) {
      return null;  // Retorna null se não encontrar o item no localStorage
    }

    let dados = null;

    // Tenta verificar se o valor pode ser um JSON válido
    try {
      dados = JSON.parse(dadosString); // Tenta fazer o parse
    } catch (e) {
      console.error(`Erro ao fazer o parse de ${key}:`, e);
      return null;  // Retorna null se o valor não for um JSON válido
    }

    // Se o valor foi parseado corretamente e possui timestamp, verifica a expiração
    if (dados && dados.timestamp && dados.data) {
      const { timestamp, data } = dados;

      // Verifica se o dado expirou
      const agora = new Date().getTime();
      if (agora - timestamp > tempoExpiracao) {
        localStorage.removeItem(key); // Remove o item se tiver expirado
        return null;  // Retorna null se expirou
      }

      return data;  // Retorna os dados se não expiraram
    }

    return null;  // Retorna null caso o formato dos dados seja inválido
  } catch (error) {
    console.error("Erro ao carregar dados com expiração:", error);
    return null;  // Retorna null caso ocorra algum erro
  }
};
