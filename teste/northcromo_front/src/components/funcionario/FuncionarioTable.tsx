import { FiEdit, FiTrash2 } from 'react-icons/fi'
import React, { useRef } from 'react'

interface Funcionario {
  id: number
  nome: string
  funcao: string
  status: 'ativo' | 'inativo'
}

interface FuncionarioTableProps {
  funcionarios?: Funcionario[]
  loading?: boolean;
  selecionados?: number[]
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  idEditar: number | null
  modoEdicaoMultipla: boolean
  setModoEdicaoMultipla: React.Dispatch<React.SetStateAction<boolean>>;
  editaveis: Funcionario[]
  setEditaveis: React.Dispatch<React.SetStateAction<Funcionario[]>>
  onEdit: (func: Funcionario) => void
  onDelete: (id: number) => void
  onSalvarEdicao: (funcEditado: Funcionario) => void
  onCancelarEdicao: () => void
  onDeleteEmMassa: (ids: number[]) => void
  onEditarEmMassa: (funcs: Funcionario[]) => void
}


export default function FuncionarioTable({
  funcionarios = [],
  selecionados = [],
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
  onEditarEmMassa, // MENSAGEM NA TABELA
  loading = false,
}: FuncionarioTableProps) {

  const refsInputs = useRef<(HTMLInputElement | null)[]>([])

  const onKeyDownCell = (
  e: React.KeyboardEvent,
  currentIndex: number,
  totalColumns: number
) => {
  if (e.key === 'Enter') {
    e.preventDefault()

    // SHIFT + Enter vai para cima, Enter vai para baixo
    const direction = e.shiftKey ? -totalColumns : totalColumns
    const nextIndex = currentIndex + direction

    const nextInput = refsInputs.current[nextIndex]
    if (nextInput) {
      // garante que o input existe e está montado
      setTimeout(() => nextInput?.focus(), 0)
    }
  }

  if (e.key === 'Tab') {
    const direction = e.shiftKey ? -1 : 1
    const nextIndex = currentIndex + direction
    const nextInput = refsInputs.current[nextIndex]
    if (nextInput) {
      e.preventDefault()
      setTimeout(() => nextInput?.focus(), 0)
    }
  }
}

  return (
    <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
      {selecionados.length > 0 && !modoEdicaoMultipla && (
        <div className="flex justify-between items-center bg-gray-100 p-3 rounded-md mb-3 shadow-sm">
          <span className="text-sm text-gray-700">
            {selecionados.length} funcionário(s) selecionado(s)
          </span>
          <div className="flex gap-3">
            <button
              onClick={() => {
                const paraEditar = funcionarios.filter(f => selecionados.includes(f.id))
                setEditaveis(paraEditar)
                setModoEdicaoMultipla(true)
                 refsInputs.current = []
              }}
              className="bg-blue-600 text-white px-4 py-1 rounded hover:bg-blue-700 text-sm"
              aria-label="Editar selecionados"
            >
              Editar Selecionados
            </button>
            <button
              onClick={() => onDeleteEmMassa(selecionados)}
              className="bg-red-600 text-white px-4 py-1 rounded hover:bg-red-700 text-sm"
              aria-label="Excluir selecionados"
            >
              Excluir Selecionados
            </button>
          </div>
        </div>
      )}

      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">Nome Funcionario</th>
            <th className="px-4 py-2 text-left">Grupo_Responsavel</th>
            <th className="px-4 py-2 text-left">Status</th>
            <th className="px-4 py-2 text-left">Ações</th>
            <th className="px-4 py-2 text-center">
              <input
                type="checkbox"
                checked={todosSelecionados}
                onChange={toggleSelecionarTodos}
                className="accent-green-600 w-5 h-5"
                aria-label="Selecionar todos"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {loading ? (
          <tr>
          <td colSpan={5} className="text-center p-4">
            Carregando funcionários...
          </td>
        </tr>
          ) :funcionarios.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum funcionário cadastrado.
              </td>
            </tr>
          ) :
          (
            funcionarios.map((func, index)  => {
              const estaEditando = idEditar === func.id
              const emEdicaoMultipla = modoEdicaoMultipla && selecionados.includes(func.id)
              const editavel = editaveis.find(f => f.id === func.id)
              const baseIndex = index * 3 // nome, funcao, status
              return (
                <tr
                  key={func.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${
                    (estaEditando || emEdicaoMultipla) ? 'bg-yellow-100' : ''
                  }`}
                >
                  {/* Nome */}
                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <input
                        type="text"
                        ref={(el) => refsInputs.current[baseIndex + 0] = el} // cada funcionário tem 3 campos
                        value={editavel?.nome || ''}
                        onChange={e =>
                          setEditaveis(prev =>
                            prev.map(f => f.id === func.id ? { ...f, nome: e.target.value } : f)
                          )
                        }
                        onKeyDown={(e) => onKeyDownCell(e, baseIndex + 0, 3)}
                        onBlur={() => {
                        if (!modoEdicaoMultipla) {
                          const atual = editaveis.find(f => f.id === func.id)
                          if (atual) onSalvarEdicao(atual)
                         }
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar nome do funcionário ${func.nome}`}
                      />
                    ) : (
                      func.nome
                    )}
                  </td>

                  {/* funcao */}
                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <input
                        type="text"
                        ref={(el) => refsInputs.current[baseIndex + 1] = el} // CORRETO
                        value={editavel?.funcao || ''}
                        onChange={e =>
                          setEditaveis(prev =>
                            prev.map(f => f.id === func.id ? { ...f, funcao: e.target.value } : f)
                          )
                        }
                        onKeyDown={(e) => onKeyDownCell(e, baseIndex + 1, 3)}
                        onBlur={() => {
                          const atual = editaveis.find(f => f.id === func.id)
                          if (atual) onSalvarEdicao(atual)
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar funcao do funcionário ${func.nome}`}
                      />
                    ) : (
                      func.funcao
                    )}
                  </td>

                  {/* Status */}
                  <td className="px-4 py-2 capitalize">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <select
                        value={editavel?.status || 'ativo'}
                        onChange={e => {
                          const novoStatus = e.target.value as 'ativo' | 'inativo'
                          setEditaveis(prev =>
                            prev.map(f => f.id === func.id ? { ...f, status: novoStatus } : f)
                          )
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar status do funcionário ${func.nome}`}
                      >
                        <option value="ativo">Ativo</option>
                        <option value="inativo">Inativo</option>
                      </select>
                    ) : (
                      func.status
                    )}
                  </td>

                  {/* Ações */}
                  <td className="px-4 py-2 flex gap-2">
                    {!modoEdicaoMultipla && !estaEditando && (
                      <>
                        <button
                          onClick={() => onEdit(func)}
                          className="text-blue-600 hover:text-blue-800"
                          title="Editar"
                          aria-label={`Editar funcionário ${func.nome}`}
                        >
                          <FiEdit />
                        </button>
                        <button
                          onClick={() => onDelete(func.id)}
                          className="text-red-600 hover:text-red-800"
                          title="Excluir"
                          aria-label={`Excluir funcionário ${func.nome}`}
                        >
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </td>

                  {/* Checkbox */}
                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(func.id)}
                      onChange={() => toggleSelecionado(func.id)}
                      className="accent-green-600 w-5 h-5"
                      aria-label={`Selecionar funcionário ${func.nome}`}
                    />
                  </td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>

      {/* Ações em massa */}
      {modoEdicaoMultipla && (
        <div className="flex gap-4 mt-4">
          <button
            onClick={() => {
              const editados = editaveis.filter(f => selecionados.includes(f.id))
              onEditarEmMassa(editados)
            }}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-800"
          >
            Salvar Edição Múltipla
          </button>
          <button
            onClick={onCancelarEdicao}
            className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  )
}
