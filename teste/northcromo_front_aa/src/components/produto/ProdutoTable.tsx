import React from 'react';
import { FiEdit, FiTrash2 } from 'react-icons/fi';

// Definição das interfaces auxiliares, baseadas no uso no componente:
interface Componente {
  id: number;
  nome: string;
  componente_nome?: string; // pode aparecer em item.componente.componente_nome
}

interface Operacao {
  id: number;
  nome: string;
  op_nome?: string; // pode aparecer em item.operacao.op_nome
}

interface PostoTrabalho {
  id: number;
  nome: string;
  posto_trabalho_nome?: string; // pode aparecer em item.posto_trabalho.posto_trabalho_nome
}

interface Produto {
  id: number;
  cod_produto: string | number;
  produto_nome: string;
  componente?: Componente;
  componente_id?: number;
  operacao?: Operacao;
  operacao_id?: number;
  posto_trabalho?: PostoTrabalho;
  posto_trabalho_id?: number;
  tipo_produto: number;
}

// Props do componente
interface ProdutoTableProps {
  produtos: Produto[];
  selecionados: number[];
  toggleSelecionado: (id: number) => void;
  toggleSelecionarTodos: () => void;
  todosSelecionados: boolean;
  idEditar: number | null;
  modoEdicaoMultipla: boolean;
  editaveis: Produto[];
  setEditaveis: React.Dispatch<React.SetStateAction<Produto[]>>;
  onEditar: (item: Produto) => void;
  onDelete: (id: number) => void;
  onSalvarEdicao: (item: Produto) => void;
  onCancelarEdicao: () => void;
  onDeleteEmMassa: (ids: number[]) => void;
  onEditarEmMassa: (itens: Produto[]) => void;
  componentes: Componente[];
  operacoes: Operacao[];
  postosTrabalho: PostoTrabalho[];
}

const ProdutoTable: React.FC<ProdutoTableProps> = ({
  produtos,
  selecionados,
  toggleSelecionado,
  toggleSelecionarTodos,
  todosSelecionados,
  idEditar,
  modoEdicaoMultipla,
  editaveis,
  setEditaveis,
  onEditar,
  onDelete,
  onSalvarEdicao,
  onCancelarEdicao,
  onDeleteEmMassa,
  onEditarEmMassa,
  componentes,
  operacoes,
  postosTrabalho,
}) => {
  return (
    <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
      {selecionados.length > 0 && !modoEdicaoMultipla && (
        <div className="flex justify-between items-center bg-gray-100 p-3 rounded-md mb-3 shadow-sm">
          <span className="text-sm text-gray-700">{selecionados.length} item(ns) selecionado(s)</span>
          <div className="flex gap-3">
            <button
              onClick={() => {
                const selecionadosParaEditar = produtos.filter(p => selecionados.includes(p.id));
                setEditaveis(selecionadosParaEditar);
                onEditarEmMassa(selecionadosParaEditar);
              }}
              className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700 text-sm"
            >
              Editar Selecionados
            </button>
            <button
              onClick={() => onDeleteEmMassa(selecionados)}
              className="bg-red-600 text-white px-4 py-1 rounded hover:bg-red-700 text-sm"
            >
              Excluir Selecionados
            </button>
          </div>
        </div>
      )}

      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">Código</th>
            <th className="px-4 py-2 text-left">Nome</th>
            <th className="px-4 py-2 text-left">Componente</th>
            <th className="px-4 py-2 text-left">Operação</th>
            <th className="px-4 py-2 text-left">Posto de Trabalho</th>
            <th className="px-4 py-2 text-left">Tipo</th>
            <th className="px-4 py-2 text-left">Ações</th>
            <th className="px-4 py-2 text-center">
              <input
                type="checkbox"
                checked={todosSelecionados}
                onChange={toggleSelecionarTodos}
                className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
                aria-label="Selecionar todos"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {produtos.length === 0 ? (
            <tr>
              <td colSpan={8} className="text-center p-4">
                Nenhum produto cadastrado.
              </td>
            </tr>
          ) : (
            produtos.map(item => {
              const estaEditando = idEditar === item.id;
              const emEdicaoMultipla = modoEdicaoMultipla && selecionados.includes(item.id);
              const editavelItem = editaveis.find(e => e.id === item.id);

              return (
                <tr
                  key={item.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${estaEditando || emEdicaoMultipla ? 'bg-yellow-100' : ''}`}
                >
                  <td className="px-4 py-2">{item.cod_produto}</td>

                  <td className="px-4 py-2">{item.produto_nome}</td>

                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <select
                        value={editavelItem?.componente_id || 0}
                        onChange={e => {
                          const novoId = Number(e.target.value);
                          const nomeSelecionado = componentes.find(c => c.id === novoId)?.nome || '';
                          setEditaveis(prev =>
                            prev.map(el =>
                              el.id === item.id
                                ? { ...el, componente_id: novoId, componente: { id: novoId, nome: nomeSelecionado } }
                                : el
                            )
                          );
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find(el => el.id === item.id);
                          if (editItem) onSalvarEdicao(editItem);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      >
                        {componentes.map(c => (
                          <option key={c.id} value={c.id}>{c.nome}</option>
                        ))}
                      </select>
                    ) : (
                      item.componente?.componente_nome || ''
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <select
                        value={editavelItem?.operacao_id || 0}
                        onChange={e => {
                          const novoId = Number(e.target.value);
                          const nomeSelecionado = operacoes.find(o => o.id === novoId)?.nome || '';
                          setEditaveis(prev =>
                            prev.map(el =>
                              el.id === item.id
                                ? { ...el, operacao_id: novoId, operacao: { id: novoId, nome: nomeSelecionado } }
                                : el
                            )
                          );
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find(el => el.id === item.id);
                          if (editItem) onSalvarEdicao(editItem);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      >
                        {operacoes.map(op => (
                          <option key={op.id} value={op.id}>{op.nome}</option>
                        ))}
                      </select>
                    ) : (
                      item.operacao?.op_nome || ''
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <select
                        value={editavelItem?.posto_trabalho_id || 0}
                        onChange={e => {
                          const novoId = Number(e.target.value);
                          const nomeSelecionado = postosTrabalho.find(p => p.id === novoId)?.nome || '';
                          setEditaveis(prev =>
                            prev.map(el =>
                              el.id === item.id
                                ? { ...el, posto_trabalho_id: novoId, posto_trabalho: { id: novoId, nome: nomeSelecionado } }
                                : el
                            )
                          );
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find(el => el.id === item.id);
                          if (editItem) onSalvarEdicao(editItem);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      >
                        {postosTrabalho.map(p => (
                          <option key={p.id} value={p.id}>{p.nome}</option>
                        ))}
                      </select>
                    ) : (
                      item.posto_trabalho?.posto_trabalho_nome || ''
                    )}
                  </td>

                  <td className="px-4 py-2">{item.tipo_produto === 1 ? 'Produto' : 'Tarefa'}</td>

                  <td className="px-4 py-2 flex gap-3">
                    {!modoEdicaoMultipla && !estaEditando && (
                      <>
                        <button
                          onClick={() => onEditar(item)}
                          className="text-blue-600 hover:text-blue-800"
                          title="Editar"
                        >
                          <FiEdit />
                        </button>
                        <button
                          onClick={() => onDelete(item.id)}
                          className="text-red-600 hover:text-red-800"
                          title="Excluir"
                        >
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </td>

                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(item.id)}
                      onChange={() => toggleSelecionado(item.id)}
                      className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
                      aria-label={`Selecionar produto ${item.produto_nome}`}
                    />
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>

      {modoEdicaoMultipla && (
        <div className="flex gap-4 mt-4">
          <button
            onClick={() => {
              const itensSelecionados = editaveis.filter(item => selecionados.includes(item.id));
              if (itensSelecionados.length > 0) onEditarEmMassa(itensSelecionados);
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800"
          >
            Salvar Edição Múltipla
          </button>
          <button
            onClick={onCancelarEdicao}
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  );
};

export default ProdutoTable;
