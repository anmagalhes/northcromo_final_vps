import { RecebimentoRead } from './recebimento'
import { ComponenteRead } from './componente'
import { OperacaoItem  } from './operacao'
import { PostoTrabalhoRead } from './posto_trabalho'
import { Produto } from './produto'

export interface Checklist {
  id: number
  recebimento_id: number | null;
  item1: boolean;
  item2: boolean;
  observacoes: string | null;
  link_pdf: string | null;
  descricao: string
  tem_pdf: boolean
  os_formatado: string | null;

  recebimento?: RecebimentoRead | null
  componente?: ComponenteRead | null
  operacao?: OperacaoItem  | null
  posto_trabalho?: PostoTrabalhoRead | null
  produto?: Produto | null
}

export type ChecklistTableItem = Omit<Checklist, 'recebimento_id'> & {
  recebimento_id: string;
}
