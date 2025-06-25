import React from 'react'
import { FiEdit, FiTrash2 } from 'react-icons/fi'

interface ComponenteItem {
  id: number
  componente_nome: string
  data_recebimento: string
}

interface Props {
  componentes: ComponenteItem[]
  onEdit: (item: ComponenteItem) => void
  onDelete: (id: number) => void
  selecionados: number[]
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  idEditar: number | null
  modoEdicaoMultipla: boolean
  editaveis: ComponenteItem[]
  setEditaveis: React.Dispatch<React.SetStateAction<ComponenteItem[]>>
  onSalvarEdicao: (item: ComponenteItem) => void
  onCancelarMultiplos: () => void
  onSalvarMultiplos: () => void  // ADICIONADO AQUI
}

export default function ComponenteTable({
  componentes,
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
  onCancelarMultiplos,
  onSalvarMultiplos,  // RECEBENDO A FUNÇÃO AQUI
}: Props) {
  return (
    <>
      {/* Botões Salvar todos / Cancelar só aparecem em edição múltipla */}
      {modoEdicaoMultipla && (
        <div className="mb-4 flex gap-2 justify-end">
          <button
            onClick={onSalvarMultiplos}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
          >
            Salvar todos
          </button>
          <button
            onClick={onCancelarMultiplos}
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition"
          >
            Cancelar
          </button>
        </div>
      )}

      <div className="overflow-x-auto max-h-[400px] overflow-y-auto">
        <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
          <thead className="bg-green-700 text-white">
            <tr>
              <th className="px-4 py-2 text-left">ID</th>
              <th className="px-4 py-2 text-left">Componente</th>
              <th className="px-4 py-2 text-left">Data Recebimento</th>
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
            {componentes.length === 0 ? (
              <tr>
                <td colSpan={5} className="text-center p-4">
                  Nenhum componente cadastrado.
                </td>
              </tr>
            ) : (
              componentes.map((item) => {
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

                    {/* Campo componente_nome - texto editável */}
                    <td className="px-4 py-2">
                      {editavel ? (
                        <input
                          type="text"
                          value={editavelItem?.componente_nome || ''}
                          onChange={(e) => {
                            const novoValor = e.target.value
                            setEditaveis((prev) =>
                              prev.map((el) =>
                                el.id === item.id
                                  ? { ...el, componente_nome: novoValor }
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
                        item.componente_nome
                      )}
                    </td>

                    {/* Campo data_recebimento - input date editável */}
                    <td className="px-4 py-2">
                      {editavel ? (
                        <input
                          type="date"
                          value={
                            editavelItem
                              ? new Date(editavelItem.data_recebimento).toISOString().slice(0, 10)
                              : ''
                          }
                          onChange={(e) => {
                            const novaData = e.target.value
                            setEditaveis((prev) =>
                              prev.map((el) =>
                                el.id === item.id
                                  ? { ...el, data_recebimento: novaData }
                                  : el
                              )
                            )
                          }}
                          className="border rounded px-2 py-1 w-full"
                        />
                      ) : (
                        new Date(item.data_recebimento).toLocaleDateString()
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
                        className="accent-green-600 w-5 h-5 rounded border-gray-300 focus:ring-2 focus:ring-green-500"
                      />
                    </td>
                  </tr>
                )
              })
            )}
          </tbody>
        </table>
      </div>
    </>
  )
}
