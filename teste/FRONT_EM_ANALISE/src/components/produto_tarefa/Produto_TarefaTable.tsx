import React from 'react';
import { FiEdit, FiTrash2 } from 'react-icons/fi';

interface ProdutoTarefaItem {
  id: number;
  produto_taf_nome: string;
  data_execucao: string;
}

interface Props {
  tarefa: ProdutoTarefaItem[];
  onEdit: (item: ProdutoTarefaItem) => void;
  onDelete: (id: number) => void;
  selecionados: number[];
  toggleSelecionado: (id: number) => void;
  toggleSelecionarTodos: () => void;
  todosSelecionados: boolean;
  idEditar: number | null;
  modoEdicaoMultipla: boolean;
  editaveis: ProdutoTarefaItem[];
  setEditaveis: React.Dispatch<React.SetStateAction<ProdutoTarefaItem[]>>;
  onSalvarMultiplos: () => Promise<void>;
  onCancelarMultiplos: () => void;
  onSalvarEdicao: (item: ProdutoTarefaItem) => Promise<void>;
}

export default function Produto_TarefaTable({
  tarefa,
  onEdit,
  onDelete,
  selecionados,
  toggleSelecionado,
  toggleSelecionarTodos,
  todosSelecionados,
  idEditar,
  modoEdicaoMultipla,
  editaveis,
  setEditaveis,
  onSalvarMultiplos,
  onCancelarMultiplos,
  onSalvarEdicao,
}: Props) {
  // Garantir que 'tarefa' seja sempre um array
  const tarefasValidas = Array.isArray(tarefa) ? tarefa : [];

  return (
    <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
      {/* Botões para edição múltipla */}
      {modoEdicaoMultipla && (
        <div className="flex gap-4 mb-4">
          <button
            onClick={onSalvarMultiplos}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800 transition"
          >
            Salvar Edição Múltipla
          </button>
          <button
            onClick={onCancelarMultiplos}
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition"
          >
            Cancelar
          </button>
        </div>
      )}

      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">Nome Posto Trabalho</th>
            <th className="px-4 py-2 text-left">Data Execução</th>
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
          {tarefasValidas.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum posto de trabalho cadastrado.
              </td>
            </tr>
          ) : (
            tarefasValidas.map((item) => {
              const estaEditando = idEditar === item.id;
              const editavel = modoEdicaoMultipla && selecionados.includes(item.id);
              const editavelItem = editaveis.find(e => e.id === item.id);

              return (
                <tr
                  key={item.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${
                    estaEditando || editavel ? 'bg-yellow-100' : ''
                  }`}
                >
                  <td className="px-4 py-2">{item.id}</td>

                  {/* Campo produto_taf_nome */}
                  <td className="px-4 py-2">
                    {editavel ? (
                      <input
                        type="text"
                        value={editavelItem?.produto_taf_nome || ''}
                        onChange={(e) => {
                          const novoValor = e.target.value;
                          setEditaveis((prev) =>
                            prev.map((el) =>
                              el.id === item.id ? { ...el, produto_taf_nome: novoValor } : el
                            )
                          );
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find(el => el.id === item.id);
                          if (editItem) {
                            onSalvarEdicao(editItem); // salva ao sair do campo
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar nome da tarefa ${item.produto_taf_nome}`}
                      />
                    ) : (
                      item.produto_taf_nome
                    )}
                  </td>

                  {/* Campo data_execucao */}
                  <td className="px-4 py-2">
                    {editavel ? (
                      <input
                        type="date"
                        value={
                          editavelItem
                            ? new Date(editavelItem.data_execucao).toISOString().slice(0, 10)
                            : ''
                        }
                        onChange={(e) => {
                          const novaData = e.target.value;
                          setEditaveis((prev) =>
                            prev.map((el) =>
                              el.id === item.id ? { ...el, data_execucao: novaData } : el
                            )
                          );
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find(el => el.id === item.id);
                          if (editItem) {
                            onSalvarEdicao(editItem); // salva ao sair do campo
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar data da tarefa ${item.produto_taf_nome}`}
                      />
                    ) : (
                      new Date(item.data_execucao).toLocaleDateString()
                    )}
                  </td>

                  {/* Ações */}
                  <td className="px-4 py-2 flex gap-3">
                    <button
                      onClick={() => onEdit(item)}
                      className="text-blue-600 hover:text-blue-800"
                      title="Editar"
                      aria-label={`Editar tarefa ${item.produto_taf_nome}`}
                    >
                      <FiEdit />
                    </button>
                    <button
                      onClick={() => onDelete(item.id)}
                      className="text-red-600 hover:text-red-800"
                      title="Excluir"
                      aria-label={`Excluir tarefa ${item.produto_taf_nome}`}
                    >
                      <FiTrash2 />
                    </button>
                  </td>

                  {/* Checkbox seleção */}
                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(item.id)}
                      onChange={() => toggleSelecionado(item.id)}
                      className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
                      aria-label={`Selecionar tarefa ${item.produto_taf_nome}`}
                    />
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}
