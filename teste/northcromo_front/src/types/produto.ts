export interface Produto {
  id?: number
  cod_produto: string
  produto_nome: string
  data: string
  componente_id: number
  operacao_id: number
  posto_trabalho_id: number
  componente_nome?: string
  operacao_nome?: string
  posto_trabalho_nome?: string
  und_servicos?: string
  grupo_id?: string
  tipo_produto?: number
}
