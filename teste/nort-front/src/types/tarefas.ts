// src//types/tarefas.ts
export type Tarefa = {
  id: number;
  dataLancamento: string;
  numeroControle: string;
  clienteNome: string;
  quantidade: number;
  codigoProduto: string;
  descricaoProduto: string;
  operacao: string;
  observacao: string;
}


export type Produto = {
  codigo: string;
  nome: string;
  descricao: string;
  operacao: string;
}

export type Cliente = {
  id: number;
  nome: string;
}

export type Ordem = {
  id: number;
  controlNumber: string;
  receiptDate: string;
  clientName: string;
}

export type NewTarefa = Omit<Tarefa, 'id'>;


export interface TarefaCompleta {
  id: number;
  id_ordem: string; // ID_Ordem - Recebimento
  dataRec_OrdemServicos: string; // Data de recebimento
  id_cliente: string; // ID do cliente
  nome_cliente?: string; // opcional, populado por join
  qtde_servico: number;
  id_servico: string;
  nome_servico?: string;
  id_servico2?: string;
  nome_servico2?: string;
  id_operacao: string;
  nome_operacao?: string;
  desc_servico_produto: string;
  observacao: string;
  status_tarefa: 'Pendente' | 'Em Andamento' | 'Concluída'; // ou string comum
  data_lancamento: string;
  referencia_produto: string;
  nota_interna?: string;
  dataChecklist_OrdemServicos?: string;
}

