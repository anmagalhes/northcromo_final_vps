export interface Defeito {
  id: number;
  def_nome: string;
  data: string; // ISO string, pode ser convertido com dayjs, date-fns etc.
  component_id: number;
  componente_nome?: string; // pode ser undefined se o backend não enviar
}
