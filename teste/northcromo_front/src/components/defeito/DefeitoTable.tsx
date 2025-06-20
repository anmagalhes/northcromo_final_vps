import { FiEdit, FiTrash2, FiCheck, FiX } from 'react-icons/fi'
import React, { useState } from 'react'

interface Funcionario {
  id: number
  nome: string
  cargo: string
  status: 'ativo' | 'inativo'
}

interface FuncionarioTableProps {
  funcionarios?: Funcionario[]
  loading?: boolean
  selecionados?: number[]
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  idEditar: number | null
  modoEdicaoMultipla: boolean
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
  editaveis,
  setEditaveis,
  onEdit,
  onDelete,
  onSalvarEdicao,
  onCancelarEdicao,
  onDeleteEmMassa,
  onEditarEmMassa,
  loading = false,
}: FuncionarioTableProps) {
  // Estado local para validar campos na edição individual
  const [erros, setErros] = useState<{ [id: number]: { nome?: string; cargo?: string } }>({})

  // Função para validar um funcionário editável
  const validarFuncionario = (func: Funcionario) => {
    const errosLocais: { nome?: string; cargo?: string } = {}
    if (!func.nome.trim()) errosLocais.nome = 'Nome é obrigatório'
    if (!func.cargo.trim()) errosLocais.cargo = 'Cargo é obrigatório'
    return errosLocais
  }

  // Função para salvar edição individual com validação
  const salvarEdicaoIndividual = (func: Funcionario) => {
    const errosLocais = validarFuncionario(func)
    if (Object.keys(errosLocais).length > 0) {
      setErros(prev => ({ ...prev, [func.id]: errosLocais }))
      return
    }
    setErros(prev => ({ ...prev, [func.id]: {} }))
    onSalvarEdicao(func)
  }

  // Função cancelar edição individual limpa erros desse id
  const cancelarEdicaoIndividual = () => {
    setErros({})
    onCancelarEdicao()
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
                onEditarEmMassa(paraEditar)
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
            <th className="px-4 py-2 text-left">Nome</th>
            <th className="px-4 py-2 text-left">Cargo</th>
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
          ) : funcionarios.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum funcionário cadastrado.
              </td>
            </tr>
          ) : (
            funcionarios.map(func => {
              const estaEditando = idEditar === func.id
              const emEdicaoMultipla = modoEdicaoMultipla && selecionados.includes(func.id)
              const editavel = editaveis.find(f => f.id === func.id)

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
                      <>
                        <input
                          type="text"
                          value={editavel?.nome || ''}
                          onChange={e =>
                            setEditaveis(prev =>
                              prev.map(f =>
                                f.id === func.id ? { ...f, nome: e.target.value } : f
                              )
                            )
                          }
                          className={`border rounded px-2 py-1 w-full ${
                            erros[func.id]?.nome ? 'border-red-500' : ''
                          }`}
                          aria-label={`Editar nome do funcionário ${func.nome}`}
                        />
                        {erros[func.id]?.nome && (
                          <p className="text-red-600 text-xs mt-1">{erros[func.id]?.nome}</p>
                        )}
                      </>
                    ) : (
                      func.nome
                    )}
                  </td>

                  {/* Cargo */}
                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <>
                        <input
                          type="text"
                          value={editavel?.cargo || ''}
                          onChange={e =>
                            setEditaveis(prev =>
                              prev.map(f =>
                                f.id === func.id ? { ...f, cargo: e.target.value } : f
                              )
                            )
                          }
                          className={`border rounded px-2 py-1 w-full ${
                            erros[func.id]?.cargo ? 'border-red-500' : ''
                          }`}
                          aria-label={`Editar cargo do funcionário ${func.nome}`}
                        />
                        {erros[func.id]?.cargo && (
                          <p className="text-red-600 text-xs mt-1">{erros[func.id]?.cargo}</p>
                        )}
                      </>
                    ) : (
                      func.cargo
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
                            prev.map(f => (f.id === func.id ? { ...f, status: novoStatus } : f))
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
                  <td className="px-4 py-2 flex gap-2 items-center">
                    {/* Edição única */}
                    {estaEditando && (
                      <>
                        <button
                          onClick={() => {
                            if (editavel) salvarEdicaoIndividual(editavel)
                          }}
                          className="text-green-600 hover:text-green-800"
                          aria-label={`Salvar edição do funcionário ${func.nome}`}
                          title="Salvar"
                        >
                          <FiCheck />
                        </button>
                        <button
                          onClick={cancelarEdicaoIndividual}
                          className="text-red-600 hover:text-red-800"
                          aria-label={`Cancelar edição do funcionário ${func.nome}`}
                          title="Cancelar"
                        >
                          <FiX />
                        </button>
                      </>
                    )}

                    {/* Se não estiver editando e não estiver em modo edição múltipla */}
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
                      disabled={loading}
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

              // Validação básica para todos editados
              let validos = true
              const errosLocais: { [id: number]: { nome?: string; cargo?: string } } = {}
              for (const func of editados) {
                const errosFunc = validarFuncionario(func)
                if (Object.keys(errosFunc).length > 0) {
                  errosLocais[func.id] = errosFunc
                  validos = false
                }
              }

              if (!validos) {
                setErros(errosLocais)
                alert('Por favor, corrija os erros nos campos destacados antes de salvar.')
                return
              }
              setErros({})
              onEditarEmMassa(editados)
            }}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
            aria-label="Salvar edição múltipla"
          >
            Salvar edição múltipla
          </button>

          <button
            onClick={() => {
              setErros({})
              onCancelarEdicao()
            }}
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
            aria-label="Cancelar edição múltipla"
          >
            Cancelar
          </button>
        </div>
      )}
    </div>
  )
}
