// ProdutoForm.tsx
import React, { useEffect, useState } from 'react';

interface ProdutoFormProps {
  onSave: (
    codProduto: string,
    produtoNome: string,
    dataProduto: string,
    componenteId: number | null,
    operacaoId: number | null,
    postoTrabalhoId: number | null,
    undServicos: string,
    grupoId: string,
    tipoProduto: number
  ) => void;
  onCancel?: () => void;
  componentes: { id: number; nome: string }[];
  operacoes: { id: number; nome: string }[];
  postosTrabalho: { id: number; nome: string }[];
  isEditing?: boolean;
  initialData?: {
    codProduto: string;
    produtoNome: string;
    dataProduto: string;
    componenteId: number | null;
    operacaoId: number | null;
    postoTrabalhoId: number | null;
    undServicos: string;
    grupoId: string;
    tipoProduto: number;
  };
}

const ProdutoForm: React.FC<ProdutoFormProps> = ({
  onSave,
  onCancel,
  componentes,
  operacoes,
  postosTrabalho,
  isEditing = false,
  initialData,
}) => {
  const [codProduto, setCodProduto] = useState(initialData?.codProduto || '');
  const [produtoNome, setProdutoNome] = useState(initialData?.produtoNome || '');
  const [dataProduto, setDataProduto] = useState(initialData?.dataProduto || '');
  const [componenteId, setComponenteId] = useState<number | null>(initialData?.componenteId ?? null);
  const [operacaoId, setOperacaoId] = useState<number | null>(initialData?.operacaoId ?? null);
  const [postoTrabalhoId, setPostoTrabalhoId] = useState<number | null>(initialData?.postoTrabalhoId ?? null);
  const [undServicos, setUndServicos] = useState(initialData?.undServicos || '');
  const [grupoId, setGrupoId] = useState(initialData?.grupoId || 'PRODUTO');
  const [tipoProduto, setTipoProduto] = useState(initialData?.tipoProduto ?? 1);

  // Erros de validação simples
  const [erroCodProduto, setErroCodProduto] = useState<string | null>(null);
  const [erroProdutoNome, setErroProdutoNome] = useState<string | null>(null);
  const [erroComponente, setErroComponente] = useState<string | null>(null);
  const [erroOperacao, setErroOperacao] = useState<string | null>(null);
  const [erroUndServicos, setErroUndServicos] = useState<string | null>(null);
  const [erroGrupoId, setErroGrupoId] = useState<string | null>(null);

  useEffect(() => {
    setCodProduto(initialData?.codProduto || '');
    setProdutoNome(initialData?.produtoNome || '');
    setDataProduto(initialData?.dataProduto || '');
    setComponenteId(initialData?.componenteId ?? null);
    setOperacaoId(initialData?.operacaoId ?? null);
    setPostoTrabalhoId(initialData?.postoTrabalhoId ?? null);
    setUndServicos(initialData?.undServicos || '');
    setGrupoId(initialData?.grupoId || 'PRODUTO');
    setTipoProduto(initialData?.tipoProduto ?? 1);

    // Reset erros ao trocar dados iniciais
    setErroCodProduto(null);
    setErroProdutoNome(null);
    setErroComponente(null);
    setErroOperacao(null);
    setErroUndServicos(null);
    setErroGrupoId(null);
  }, [initialData]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Reset erros
    setErroCodProduto(null);
    setErroProdutoNome(null);
    setErroComponente(null);
    setErroOperacao(null);
    setErroUndServicos(null);
    setErroGrupoId(null);

    // Validações básicas
    if (!codProduto.trim()) {
      setErroCodProduto('Digite o código do produto');
      return;
    }
    if (!produtoNome.trim()) {
      setErroProdutoNome('Digite o nome do produto');
      return;
    }
    if (!componenteId) {
      setErroComponente('Selecione um componente');
      return;
    }
    if (!operacaoId) {
      setErroOperacao('Selecione uma operação');
      return;
    }
    if (!undServicos.trim()) {
      setErroUndServicos('Digite a unidade de serviço');
      return;
    }
    if (!grupoId.trim()) {
      setErroGrupoId('Selecione um grupo');
      return;
    }

    // Envia dados para o handler
    onSave(codProduto, produtoNome, dataProduto, componenteId, operacaoId, postoTrabalhoId, undServicos, grupoId, tipoProduto);

    // Limpa formulário se não for edição
    if (!isEditing) {
      setCodProduto('');
      setProdutoNome('');
      setDataProduto('');
      setComponenteId(null);
      setOperacaoId(null);
      setPostoTrabalhoId(null);
      setUndServicos('');
      setGrupoId('PRODUTO');
      setTipoProduto(1);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-5xl mx-auto bg-white p-6 rounded shadow-md">
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label className="block font-medium mb-1">Código do Produto</label>
          <input
            type="text"
            value={codProduto}
            onChange={(e) => setCodProduto(e.target.value)}
            disabled={isEditing} // não permite alterar código em edição
            className="w-full border p-2 rounded"
          />
          {erroCodProduto && <p className="text-red-500 text-sm">{erroCodProduto}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Nome do Produto</label>
          <input
            type="text"
            value={produtoNome}
            onChange={(e) => setProdutoNome(e.target.value.toUpperCase())}
            className="w-full border p-2 rounded"
          />
          {erroProdutoNome && <p className="text-red-500 text-sm">{erroProdutoNome}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Data do Produto</label>
          <input
            type="date"
            value={dataProduto}
            onChange={(e) => setDataProduto(e.target.value)}
            className="w-full border p-2 rounded"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label className="block font-medium mb-1">Componente</label>
          <select
            value={componenteId ?? ''}
            onChange={(e) => setComponenteId(Number(e.target.value))}
            className="w-full border p-2 rounded"
          >
            <option value="">Selecione um componente</option>
            {componentes.map((comp) => (
              <option key={comp.id} value={comp.id}>
                {comp.nome}
              </option>
            ))}
          </select>
          {erroComponente && <p className="text-red-500 text-sm">{erroComponente}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Operação</label>
          <select
            value={operacaoId ?? ''}
            onChange={(e) => setOperacaoId(Number(e.target.value))}
            className="w-full border p-2 rounded"
          >
            <option value="">Selecione uma operação</option>
            {operacoes.map((op) => (
              <option key={op.id} value={op.id}>
                {op.nome}
              </option>
            ))}
          </select>
          {erroOperacao && <p className="text-red-500 text-sm">{erroOperacao}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Posto de Trabalho</label>
          <select
            value={postoTrabalhoId ?? ''}
            onChange={(e) => setPostoTrabalhoId(Number(e.target.value))}
            className="w-full border p-2 rounded"
          >
            <option value="">Selecione um posto de trabalho</option>
            {postosTrabalho.map((posto) => (
              <option key={posto.id} value={posto.id}>
                {posto.nome}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div>
          <label className="block font-medium mb-1">Unidade de Serviço</label>
          <input
            type="text"
            value={undServicos}
            onChange={(e) => setUndServicos(e.target.value)}
            className="w-full border p-2 rounded"
          />
          {erroUndServicos && <p className="text-red-500 text-sm">{erroUndServicos}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Grupo</label>
          <select
            value={grupoId}
            onChange={(e) => setGrupoId(e.target.value)}
            className="w-full border p-2 rounded"
          >
            <option value="">Selecione o grupo</option>
            <option value="PRODUTO">Produto</option>
            <option value="SERVIÇO">Serviço</option>
          </select>
          {erroGrupoId && <p className="text-red-500 text-sm">{erroGrupoId}</p>}
        </div>

        <div>
          <label className="block font-medium mb-1">Tipo de Produto</label>
          <select
            value={tipoProduto}
            onChange={(e) => setTipoProduto(Number(e.target.value))}
            className="w-full border p-2 rounded"
          >
            <option value="">Selecione o tipo</option>
            <option value={1}>Produto</option>
            <option value={2}>Tarefa</option>
          </select>
        </div>
      </div>

      <div className="flex gap-4 mt-4">
        <button
          type="submit"
          className={`flex-grow py-2 rounded text-white ${
            isEditing ? 'bg-blue-700 hover:bg-blue-800' : 'bg-green-700 hover:bg-green-800'
          }`}
        >
          {isEditing ? 'Salvar' : 'Adicionar'}
        </button>

        {isEditing && onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex-grow py-2 rounded bg-gray-400 hover:bg-gray-500 text-white"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
};

export default ProdutoForm;
