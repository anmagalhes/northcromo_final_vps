'use client';
import React, { useRef, useCallback } from 'react';
import { FiEdit, FiTrash2 } from 'react-icons/fi';
import { Funcionario, Funcao } from '@/types/funcionario';

interface FuncionarioTableProps {
  funcionarios: (Funcionario & { funcao_nome: string })[];
  funcoes: Funcao[];
  loading: boolean;
  selecionados: number[];
  toggleSelecionado: (id: number) => void;
  toggleSelecionarTodos: () => void;
  todosSelecionados: boolean;
  idEditar: number | null;
  modoEdicaoMultipla: boolean;
  setModoEdicaoMultipla: React.Dispatch<React.SetStateAction<boolean>>;
  editaveis: Funcionario[];
  setEditaveis: React.Dispatch<React.SetStateAction<Funcionario[]>>;
  onEdit: (func: Funcionario) => void;
  onDelete: (id: number) => void;
  onSalvarEdicao: (f: Funcionario) => void;
  onCancelarEdicao: () => void;
  onDeleteEmMassa: (ids: number[]) => void;
  onEditarEmMassa: (funcs: Funcionario[]) => void;
}

export default function FuncionarioTable({
  funcionarios,
  funcoes,
  loading,
  selecionados,
  toggleSelecionado,
  toggleSelecionarTodos,
  todosSelecionados,
  idEditar,
  modoEdicaoMultipla,
  setModoEdicaoMultipla,
  editaveis,
  setEditaveis,
  onEdit,
  onDelete,
  onSalvarEdicao,
  onCancelarEdicao,
  onDeleteEmMassa,
  onEditarEmMassa,
}: FuncionarioTableProps) {
  const refs = useRef<(HTMLInputElement | HTMLSelectElement)[]>([]);

  const onKeyDownCell = useCallback(
    (e: React.KeyboardEvent, idx: number, cols: number) => {
      e.preventDefault();
      const shift = e.shiftKey;
      const dir = e.key === 'Enter' ? (shift ? -cols : cols) : shift ? -1 : 1;
      const nextIdx = idx + dir;
      const next = refs.current[nextIdx];
      if (next) {
        setTimeout(() => next.focus(), 0);
      }
    },
    []
  );

  return (
    <div className="overflow-x-auto max-h-[600px]">
      {selecionados.length > 0 && !modoEdicaoMultipla && (
        <div className="flex justify-between bg-gray-100 p-3 rounded mb-3">
          <span>{selecionados.length} selecionado(s)</span>
          <div className="flex gap-2">
            <button
              onClick={() => {
                const paraEditar = funcionarios.filter((f) => selecionados.includes(f.id));
                setEditaveis(paraEditar);
                setModoEdicaoMultipla(true);
                refs.current = [];
              }}
              className="bg-blue-600 text-white px-4 py-1 rounded"
            >
              Editar Selecionados
            </button>
            <button
              onClick={() => onDeleteEmMassa(selecionados)}
              className="bg-red-600 text-white px-4 py-1 rounded"
            >
              Excluir Selecionados
            </button>
          </div>
        </div>
      )}

      <table className="w-full table-auto border rounded">
        <thead className="bg-green-700 text-white">
          <tr>
            <th>Nome</th>
            <th>Função</th>
            <th>Status</th>
            <th>Ações</th>
            <th>
              <input type="checkbox" checked={todosSelecionados} onChange={toggleSelecionarTodos} />
            </th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
            <tr>
              <td colSpan={5} className="text-center p-6 text-gray-500">
                <div className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5 text-green-600" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
                  </svg>
                  Carregando...
                </div>
              </td>
            </tr>
          ) : funcionarios.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum funcionário cadastrado.
              </td>
            </tr>
          ) : (
            funcionarios.map((func, idx) => {
              const isSingleEdit = idEditar === func.id;
              const isMultiEdit = modoEdicaoMultipla && selecionados.includes(func.id);
              const editavel = editaveis.find((f) => f.id === func.id);
              const base = idx * 3;

              return (
                <tr key={func.id} className={isSingleEdit || isMultiEdit ? 'bg-yellow-100' : ''}>
                  <td className="px-4 py-2">
                    {isSingleEdit || isMultiEdit ? (
                      <input
                        ref={(el) => {
                          if (el) refs.current[base] = el;
                        }}
                        value={editavel?.nome || ''}
                        onChange={(e) =>
                          setEditaveis((prev) =>
                            prev.map((f) => (f.id === func.id ? { ...f, nome: e.target.value } : f))
                          )
                        }
                        onKeyDown={(e) => onKeyDownCell(e, base, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) onSalvarEdicao(editavel!);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      />
                    ) : (
                      func.nome
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {isSingleEdit || isMultiEdit ? (
                      <select
                        ref={(el) => {
                          if (el) refs.current[base + 1] = el;
                        }}
                        value={editavel?.funcao_id || ''}
                        onChange={(e) =>
                          setEditaveis((prev) =>
                            prev.map((f) => (f.id === func.id ? { ...f, funcao_id: +e.target.value } : f))
                          )
                        }
                        onKeyDown={(e) => onKeyDownCell(e, base + 1, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) onSalvarEdicao(editavel!);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      >
                        {funcoes.map((f) => (
                          <option key={f.id} value={f.id}>
                            {f.funcao_nome}
                          </option>
                        ))}
                      </select>
                    ) : (
                      func.funcao_nome
                    )}
                  </td>

                  <td className="px-4 py-2">
                    {isSingleEdit || isMultiEdit ? (
                      <select
                        ref={(el) => {
                          if (el) refs.current[base + 2] = el;
                        }}
                        value={editavel?.status || 'ATIVO'}
                        onChange={(e) =>
                          setEditaveis((prev) =>
                            prev.map((f) =>
                              f.id === func.id ? { ...f, status: e.target.value as 'ATIVO' | 'INATIVO' } : f
                            )
                          )
                        }
                        onKeyDown={(e) => onKeyDownCell(e, base + 2, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) onSalvarEdicao(editavel!);
                        }}
                        className="border rounded px-2 py-1 w-full"
                      >
                        <option value="ATIVO">Ativo</option>
                        <option value="INATIVO">Inativo</option>
                      </select>
                    ) : (
                      func.status
                    )}
                  </td>

                  <td className="px-4 py-2 flex gap-2">
                    {!modoEdicaoMultipla && !isSingleEdit && (
                      <>
                        <button onClick={() => onEdit(func)}>
                          <FiEdit />
                        </button>
                        <button onClick={() => onDelete(func.id)}>
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </td>

                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(func.id)}
                      onChange={() => toggleSelecionado(func.id)}
                    />
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>

      {modoEdicaoMultipla && (
        <div className="mt-4 flex gap-3">
          <button
            onClick={() => onEditarEmMassa(editaveis.filter((f) => selecionados.includes(f.id)))}
            className="bg-blue-600 text-white px-4 py-2"
          >
            Salvar Edição Múltipla
          </button>
          <button onClick={onCancelarEdicao} className="bg-gray-500 text-white px-4 py-2">
            Cancelar
          </button>
        </div>
      )}
    </div>
  );
}
