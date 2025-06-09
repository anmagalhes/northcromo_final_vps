import { FiEdit, FiTrash2 } from 'react-icons/fi'

interface OperacaoItem {
  id: number
  op_nome: string
  op_grupo_processo: string
  data_execucao: string
}

interface Props {
  operacoes: OperacaoItem[]
  onEdit: (item: OperacaoItem) => void
  onDelete: (id: number) => void
  selecionados: number[]
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  idEditar: number | null
  modoEdicaoMultipla: boolean
  editaveis: OperacaoItem[]
  setEditaveis: React.Dispatch<React.SetStateAction<OperacaoItem[]>>
  onSalvarEdicao: (item: OperacaoItem) => void
}

export default function OperacaoTable({
  operacoes,
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
  onSalvarEdicao,
}: Props) {
  return (
    <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">ID</th>
            <th className="px-4 py-2 text-left">Grupo Processo</th>
            <th className="px-4 py-2 text-left">Nome Operação</th>
            <th className="px-4 py-2 text-left">Data Execução</th>
            <th className="px-4 py-2 text-left">Ações</th>
            <th className="px-4 py-2 text-center">
              <input
                type="checkbox"
                checked={todosSelecionados}
                onChange={toggleSelecionarTodos}
                className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          {operacoes.length === 0 ? (
            <tr>
              <td colSpan={6} className="text-center p-4">
                Nenhuma operação cadastrada.
              </td>
            </tr>
          ) : (
            operacoes.map((item) => {
              const estaEditando = idEditar === item.id
              const editavel = modoEdicaoMultipla && selecionados.includes(item.id)
              const editavelItem = editaveis.find((e) => e.id === item.id)

              return (
                <tr
                  key={item.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${
                    estaEditando ? 'bg-yellow-100' : ''
                  }`}
                >
                  <td className="px-4 py-2">{item.id}</td>
                  {/* Campo op_grupo_processo */}
                  <td className="px-4 py-2">
                    {editavel ? (
                      <input
                        type="text"
                        value={editavelItem?.op_grupo_processo || ''}
                        onChange={(e) => {
                          const novoValor = e.target.value
                          setEditaveis((prev) =>
                            prev.map((el) =>
                              el.id === item.id
                                ? { ...el, op_grupo_processo: novoValor }
                                : el
                            )
                          )
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find((el) => el.id === item.id)
                          if (editItem) {
                            onSalvarEdicao(editItem)
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                      />
                    ) : (
                      item.op_grupo_processo
                    )}
                  </td>

                  {/* Campo op_nome */}
                  <td className="px-4 py-2">
                    {editavel ? (
                      <input
                        type="text"
                        value={editavelItem?.op_nome || ''}
                        onChange={(e) => {
                          const novoValor = e.target.value
                          setEditaveis((prev) =>
                            prev.map((el) =>
                              el.id === item.id ? { ...el, op_nome: novoValor } : el
                            )
                          )
                        }}
                        onBlur={() => {
                          const editItem = editaveis.find((el) => el.id === item.id)
                          if (editItem) {
                            onSalvarEdicao(editItem)
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                      />
                    ) : (
                      item.op_nome
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
                          const novaData = e.target.value
                          setEditaveis((prev) =>
                            prev.map((el) =>
                              el.id === item.id
                                ? { ...el, data_execucao: novaData }
                                : el
                            )
                          )
                        }}
                        className="border rounded px-2 py-1 w-full"
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
                  </td>

                  {/* Checkbox seleção */}
                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(item.id)}
                      onChange={() => toggleSelecionado(item.id)}
                      className="accent-green-600 w-5 h-5 rounded"
                    />
                  </td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>
    </div>
  )
}
