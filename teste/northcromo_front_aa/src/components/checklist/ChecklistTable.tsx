// src/components/checklist/checklistTable.tsx

import { useRef } from 'react'
import { FiEdit, FiTrash2 } from 'react-icons/fi'
import ButtonGerarPDFs from '@/components/botao/PDFButton'
import { Checklist, ChecklistTableItem } from '@/types/checklist'

interface ChecklistTableProps {
  checklists?: ChecklistTableItem[]
  loading?: boolean
  selecionados?: number[]
  toggleSelecionado: (id: number) => void
  toggleSelecionarTodos: () => void
  todosSelecionados: boolean
  idEditar: number | null
  modoEdicaoMultipla: boolean
  setModoEdicaoMultipla: React.Dispatch<React.SetStateAction<boolean>> // REMOVIDO
  editaveis: Checklist[]
  setEditaveis: React.Dispatch<React.SetStateAction<Checklist[]>>
  onEdit: (checklist: Checklist) => void
  onDelete: (id: number) => void
  onSalvarEdicao: (checklistEditado: Checklist) => void
  onCancelarEdicao: () => void
  onDeleteEmMassa: (ids: number[]) => Promise<void>
  onEditarEmMassa: (itensEditados: Checklist[]) => Promise<void>
}

export default function ChecklistTable({
  checklists = [],
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
  onEditarEmMassa,
  loading = false,
}: ChecklistTableProps) {
  const refsInputs = useRef<(HTMLInputElement | null)[]>([])

  const onKeyDownCell = (
    e: React.KeyboardEvent,
    currentIndex: number,
    totalColumns: number
  ) => {
    if (e.key === 'Enter') {
      e.preventDefault()
      const direction = e.shiftKey ? -totalColumns : totalColumns
      const nextIndex = currentIndex + direction
      const nextInput = refsInputs.current[nextIndex]
      if (nextInput) setTimeout(() => nextInput?.focus(), 0)
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

      {/* Ações em massa (quando tem selecionados e não está editando múltiplos) */}
      {selecionados.length > 0 && !modoEdicaoMultipla && (
        <div className="flex justify-between items-center bg-gray-100 p-3 rounded-md mb-3 shadow-sm">
          <span className="text-sm text-gray-700">
            {selecionados.length} checklist(s) selecionado(s)
          </span>

          <div className="flex flex-wrap gap-3 items-center">

            {/* Checklists selecionados que NÃO têm PDF */}
            {checklists.some(item => selecionados.includes(item.id) && !item.tem_pdf) && (
              <ButtonGerarPDFs
                tipo="sem_pdf"
                selecionados={selecionados}
                checklists={checklists}
                onGenerate={() => console.log('Gerar com PDF clicado')}
              />
            )}

            {/* Checklists selecionados que JÁ têm PDF */}
            {checklists.some(item => selecionados.includes(item.id) && item.tem_pdf) && (
              <ButtonGerarPDFs
                tipo="com_pdf"
                selecionados={selecionados}
                checklists={checklists}
                onGenerate={() => console.log('Gerar sem PDF clicado')}
              />
            )}
          </div>
        </div>
      )}

      <table className="w-full table-auto border border-gray-200 rounded-md shadow-sm">
        <thead className="bg-green-700 text-white">
          <tr>
            <th className="px-4 py-2">Nº de Controle</th>
            <th className="px-4 py-2">Cliente</th>
            <th className="px-4 py-2 w-40 truncate">Produto</th>
            <th className="px-4 py-2 text-left">Recebimento ID</th>
            <th className="px-4 py-2 text-left">Descrição</th>
            <th className="px-4 py-2 text-center">Tem PDF</th>
            <th className="px-4 py-2 text-left">Ações</th>
            <th className="px-4 py-2 text-center">
              <input
                type="checkbox"
                checked={todosSelecionados}
                onChange={() => {
                  console.log('Checkbox selecionar todos toggled')
                  toggleSelecionarTodos()
                }}
                className="accent-green-600 w-5 h-5"
                aria-label="Selecionar todos"
              />
            </th>
          </tr>
        </thead>

        <tbody>
          {loading ? (
            <tr>
              <td colSpan={8} className="text-center p-4">Carregando checklists...</td>
            </tr>
          ) : checklists.length === 0 ? (
            <tr>
              <td colSpan={8} className="text-center p-4">Nenhum checklist cadastrado.</td>
            </tr>
          ) : (
            checklists.map((item, idx) => {
              const estaEditando = idEditar === item.id
              const emEdicaoMultipla = modoEdicaoMultipla && selecionados.includes(item.id)
              const editavel = editaveis.find(c => c.id === item.id)
              const baseIndex = idx * 3 // 3 colunas editáveis: recebimento_id, descricao, tem_pdf

              return (
                <tr
                  key={item.id}
                  className={`hover:bg-gray-50 border-t border-gray-200 ${
                    (estaEditando || emEdicaoMultipla) ? 'bg-yellow-100' : ''
                  }`}
                >
                  {/* Nº de Controle */}
                  <td className="px-4 py-2 w-32 truncate">{item.recebimento?.os_formatado || '-'}</td>

                  {/* Cliente */}
                  <td className="px-4 py-2 max-w-xs break-words">{item.recebimento?.cliente || '-'}</td>

                  {/* Produto Nome */}
                  <td className="px-4 py-2 w-40 truncate">
                    {item.recebimento?.produto_nome || '-'}
                  </td>

                  {/* Recebimento ID */}
                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <input
                        type="text"
                        ref={(el) => {
                          refsInputs.current[baseIndex + 0] = el
                        }}
                        value={editavel?.recebimento_id?.toString() || ''}
                        onChange={e =>
                          setEditaveis(prev =>
                            prev.map(c => c.id === item.id ? { ...c, recebimento_id: Number(e.target.value) } : c)
                          )
                        }
                        onKeyDown={e => onKeyDownCell(e, baseIndex + 0, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) {
                            const atual = editaveis.find(c => c.id === item.id)
                            if (atual) {
                              const recebimentoIdNum = Number(atual.recebimento_id)
                              onSalvarEdicao({
                                ...atual,
                                recebimento_id: isNaN(recebimentoIdNum) ? null : recebimentoIdNum,
                              })
                            }
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar recebimento ID do checklist ${item.id}`}
                      />
                    ) : (
                      item.recebimento_id
                    )}
                  </td>

                  {/* Descrição */}
                  <td className="px-4 py-2">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <input
                        type="text"
                        ref={(el) => {
                          refsInputs.current[baseIndex + 1] = el
                        }}
                        value={editavel?.descricao || ''}
                        onChange={e =>
                          setEditaveis(prev =>
                            prev.map(c => c.id === item.id ? { ...c, descricao: e.target.value } : c)
                          )
                        }
                        onKeyDown={e => onKeyDownCell(e, baseIndex + 1, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) {
                            const atual = editaveis.find(c => c.id === item.id)
                            if (atual) onSalvarEdicao(atual)
                          }
                        }}
                        className="border rounded px-2 py-1 w-full"
                        aria-label={`Editar descrição do checklist ${item.id}`}
                      />
                    ) : (
                      item.descricao
                    )}
                  </td>

                  {/* Tem PDF */}
                  <td className="px-4 py-2 text-center">
                    {(estaEditando || emEdicaoMultipla) ? (
                      <input
                        type="checkbox"
                        ref={(el) => {
                          refsInputs.current[baseIndex + 2] = el
                        }}
                        checked={editavel?.tem_pdf || false}
                        onChange={e =>
                          setEditaveis(prev =>
                            prev.map(c => c.id === item.id ? { ...c, tem_pdf: e.target.checked } : c)
                          )
                        }
                        onKeyDown={e => onKeyDownCell(e, baseIndex + 2, 3)}
                        onBlur={() => {
                          if (!modoEdicaoMultipla) {
                            const atual = editaveis.find(c => c.id === item.id)
                            if (atual) onSalvarEdicao(atual)
                          }
                        }}
                        className="accent-green-600 mx-auto"
                        aria-label={`Editar campo tem PDF do checklist ${item.id}`}
                  />
                    ) : (
                      <span>{item.tem_pdf ? 'Sim' : 'Não'}</span>
                    )}
                  </td>

                  {/* Ações */}
                  <td className="px-4 py-2 flex gap-2">
                    {!modoEdicaoMultipla && !estaEditando && (
                      <>
                        <button
                          onClick={() =>
                            onEdit({
                              ...item,
                              recebimento_id: Number(item.recebimento_id),
                            })
                          }
                          className="text-blue-600 hover:text-blue-800"
                          title="Editar"
                          aria-label={`Editar checklist ${item.id}`}
                        >
                          <FiEdit />
                        </button>
                        <button
                          onClick={() => onDelete(item.id)}
                          className="text-red-600 hover:text-red-800"
                          title="Excluir"
                          aria-label={`Excluir checklist ${item.id}`}
                        >
                          <FiTrash2 />
                        </button>
                      </>
                    )}
                  </td>

                  {/* Checkbox seleção */}
                  <td className="px-4 py-2 text-center">
                    <input
                      type="checkbox"
                      checked={selecionados.includes(item.id)}
                      onChange={() => {
                        console.log('Checkbox toggled para ID:', item.id)
                        toggleSelecionado(item.id)
                      }}
                      className="accent-green-600 w-5 h-5"
                      aria-label={`Selecionar checklist ${item.id}`}
                    />
                  </td>
                </tr>
              )
            })
          )}
        </tbody>
      </table>

      {/* Controles edição múltipla */}
      {modoEdicaoMultipla && (
        <div className="flex gap-4 mt-4">
          <button
            onClick={() => {
              const editados = editaveis
                .filter(c => selecionados.includes(c.id))
                .map(c => {
                  const recebimentoIdNum = Number(c.recebimento_id)
                  return {
                    ...c,
                    recebimento_id: isNaN(recebimentoIdNum) ? null : recebimentoIdNum,
                  }
                })
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
