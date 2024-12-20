// src/utils/salva_component_com_expiracao.ts
import { Cliente }from 'src/types/Cliente'; // Importa a interface

// Função para salvar dados com expiração
export const salvarComExpiracao = (key: string, data: Cliente, expirarEmMs: number): void => {
  // Normaliza os dados para garantir que campos vazios se tornem null
  const dadosNormalizados: Cliente = {
    id: data.id, // O ID não precisa ser alterado
    nome: data.nome.trim() === '' ? null : data.nome,  // Se nome estiver vazio, salva como null
    email: data.email.trim() === '' ? null : data.email,  // Se email estiver vazio, salva como null
    telefone: data.telefone.trim() === '' ? null : data.telefone,  // Se telefone estiver vazio, salva como null
  };

  const expiracao = Date.now() + expirarEmMs; // Calcula o tempo de expiração
  const dadosComExpiracao = {
    data: dadosNormalizados,  // Dados reais normalizados
    expiracao,                // Tempo de expiração
  };

  try {
    // Serializa o objeto e armazena no localStorage
    localStorage.setItem(key, JSON.stringify(dadosComExpiracao));
    console.log(`${key} salvo com expiração no localStorage:`, dadosComExpiracao);
  } catch (error) {
    console.error(`Erro ao salvar dados de ${key} no localStorage:`, error);
  }
};
Explicação do Código
Normalização dos Dados:
Cada campo (nome, email, telefone) é verificado com trim() para garantir que espaços vazios sejam removidos. Se o campo for uma string vazia após o trim(), o valor será substituído por null.
Estrutura de Dados:
A interface Cliente agora permite que nome, email e telefone sejam null (caso os campos fiquem vazios).
Armazenamento no localStorage:
Após normalizar os dados, a função calcula o tempo de expiração (expirarEmMs) e armazena os dados no localStorage como um JSON.
3. Carregar os Dados (Função de Carregamento)
Caso você precise também de uma função para carregar os dados com verificação de expiração, você pode usá-la assim:

typescript
Copiar código
// src/utils/salva_component_com_expiracao.ts
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


// Função para carregar dados com verificação de expiração
// src/utils/salva_component_com_expiracao.ts
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