import React from 'react'
import { FiEdit, FiTrash2 } from 'react-icons/fi'

import { Defeito } from '@/types/defeito'
import { Componente } from '@/types/componente'

interface DefeitoTableProps {
  defeitos?: Defeito[]
  loading?: boolean
  selecionados?: number[]
  idEditar: number | null
  modoEdicaoMultipla: boolean
  editaveis: Defeito[]
  setEditaveis: React.Dispatch<React.SetStateAction<Defeito[]>>
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  onEdit: (defeito: Defeito) => void
  onDelete: (id: number) => void
  onSalvarEdicao: (defeito: Defeito) => void
  onCancelarEdicao: () => void
  componentes: Componente[]
  onDeleteEmMassa: (ids: number[]) => void
  onEditarEmMassa: (defeitos: Defeito[]) => void
  iniciarEdicaoMultipla: () => void
  selecionadosSet: React.Dispatch<React.SetStateAction<number[]>>

}

export default function DefeitoTable({
  defeitos = [],
  selecionados = [],
  toggleSelecionado,
  toggleSelecionarTodos,
  todosSelecionados,
  onEdit,
  onDelete,
  loading = false,
}: DefeitoTableProps) {
  return (
    <div className="overflow-x-auto max-h-[600px] overflow-y-auto">
      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2 text-left">Nome</th>
            <th className="px-4 py-2 text-left">Data</th>
            <th className="px-4 py-2 text-left">Componente</th>
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
                Carregando defeitos...
              </td>
            </tr>
          ) : defeitos.length === 0 ? (
            <tr>
              <td colSpan={5} className="text-center p-4">
                Nenhum defeito cadastrado.
              </td>
            </tr>
          ) : (
            defeitos.map(defeito => (
              <tr
                key={defeito.id}
                className="hover:bg-gray-50 border-t border-gray-200"
              >
                <td className="px-4 py-2">{defeito.def_nome}</td>
                <td className="px-4 py-2">{new Date(defeito.data).toLocaleDateString()}</td>
                <td className="px-4 py-2">{defeito.componente_nome || '—'}</td>
                <td className="px-4 py-2 flex gap-2 items-center">
                  <button
                    onClick={() => onEdit(defeito)}
                    className="text-blue-600 hover:text-blue-800"
                    title="Editar"
                    aria-label={`Editar defeito ${defeito.def_nome}`}
                  >
                    <FiEdit />
                  </button>
                  <button
                    onClick={() => onDelete(defeito.id)}
                    className="text-red-600 hover:text-red-800"
                    title="Excluir"
                    aria-label={`Excluir defeito ${defeito.def_nome}`}
                  >
                    <FiTrash2 />
                  </button>
                </td>
                <td className="px-4 py-2 text-center">
                  <input
                    type="checkbox"
                    checked={selecionados.includes(defeito.id)}
                    onChange={() => toggleSelecionado(defeito.id)}
                    className="accent-green-600 w-5 h-5"
                    aria-label={`Selecionar defeito ${defeito.def_nome}`}
                    disabled={loading}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  )
}
