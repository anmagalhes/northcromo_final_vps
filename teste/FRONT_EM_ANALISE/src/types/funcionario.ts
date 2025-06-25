// src/types/funcionario.ts

export interface Funcao {
  id: number;
  funcao_nome: string;
}

export interface FuncionarioCadastro {
  nome: string;
  funcao_id: number;
  setor_nome?: string;
  data_cadastro: string;
}

export interface Funcionario extends FuncionarioCadastro {
  id: number;
  status?: 'ATIVO' | 'INATIVO';
  funcao_rel?: Funcao;       // Relacionamento vindo da API
  funcao_nome?: string;      // Opcional, pode ser calculado no frontend
}

// Caso precise de campos como cargo, setor_id, data_admissao separados, crie outro tipo, por exemplo:

export interface FuncionarioDetalhado extends Funcionario {
  cargo: string;
  data_admissao: string;
  setor_id: number;
  setor_nome?: string;
}
