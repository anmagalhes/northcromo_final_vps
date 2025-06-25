// src/app/checklist/page.tsx

'use client'

import React, { useState } from 'react' // removido useEffect pois não é usado
import ChecklistForm from '@/components/checklist/ChecklistForm'
import ChecklistTable from '@/components/checklist/ChecklistTable'
import ModalNotificacao from '@/components/ModalNotificacao'
import { Checklist } from '@/types/checklist';
import useChecklistWS from '@/hooks/useChecklistWS';
import axios from 'axios'

/**
 * Página principal do módulo Checklist
 * Responsável por exibir, cadastrar, editar, excluir e filtrar checklists.
 */
export default function ChecklistPage() {
  // Estados de paginação e filtros
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(20)
  const [comPdfFilter, setComPdfFilter] = useState<'true' | 'false' | 'all'>('all')

  // Hook customizado para buscar os checklists via WebSocket ou API
  const { checklistsQuery } = useChecklistWS(page, limit, comPdfFilter)
  const checklists = checklistsQuery.data?.data || []

  // Estados do formulário para cadastro/edição de checklist
  const [recebimentoId, setRecebimentoId] = useState<string | number>("");
  const [descricao, setDescricao] = useState('')
  const [temPdf, setTemPdf] = useState(false)

  // Notificações e mensagens de erro
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [erro, setErro] = useState<string>('');


  // Estados para seleção e edição
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<Checklist[]>([])
  const [loading, setLoading] = useState(false)

  // Opções únicas de recebimento para filtro (sem duplicatas)
  const recebimentosOptions = Array.from(new Set(checklists.map(c => c.recebimento_id)))

  // Filtra checklists pelo recebimentoId do formulário, se preenchido
  const checklistsFiltrados = recebimentoId !== ''
  ? checklists.filter(c => c.recebimento_id === recebimentoId)
  : checklists

  // Verifica se todos os checklists filtrados estão selecionados
  const todosSelecionados = selecionados.length === checklistsFiltrados.length && checklistsFiltrados.length > 0

  /**
   * Limpa os campos do formulário para cadastro/edição
   */
  const limparCampos = () => {
    setRecebimentoId('')
    setDescricao('')
    setTemPdf(false)
    setErro('')
  }

  /**
   * Envia um novo checklist para cadastro via API
   */
  const handleEnviar = async () => {
    if (!recebimentoId || !descricao) {
      setErro('Preencha todos os campos')
      return
    }

    setLoading(true)
    setErro('')

    try {
      await axios.post('http://localhost:8000/api/checklist', {
        recebimento_id: recebimentoId,
        descricao,
        tem_pdf: temPdf,
      })
      limparCampos()
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklist cadastrado com sucesso!')
      setModalVisivel(true)
    } catch {
      setErro('Erro ao salvar checklist')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Inicia edição de um checklist individual
   * @param item Checklist a ser editado
   */
  const handleEdit = (item: Checklist) => {
    setIdEditar(item.id)
    setEditaveis([item])
    setModoEdicaoMultipla(false)
    setSelecionados([])
  }

  /**
   * Salva edição de checklist individual via API
   * @param editado Checklist editado
   */
  const handleSalvarEdicao = async (editado: Checklist) => {
    setLoading(true)
    setErro('')
    try {
      await axios.put(`http://localhost:8000/api/checklist/${editado.id}`, editado)
      setIdEditar(null)
      setEditaveis([])
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklist editado com sucesso!')
      setModalVisivel(true)
    } catch (err) {
      console.error(err)
      setErro('Erro ao salvar edição')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Cancela a edição atual
   */
  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
  }

  /**
   * Exclui checklist individual via API
   * @param id ID do checklist a excluir
   */
  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`http://localhost:8000/api/checklist/${id}`)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklist excluído com sucesso!')
      setModalVisivel(true)
    } catch (err) {
      console.error(err)
      setErro('Erro ao excluir checklist')
    }
  }

  /**
   * Exclui múltiplos checklists via API
   * @param ids IDs dos checklists a excluir
   */
  const excluirChecklistEmMassa = async (ids: number[]) => {
    try {
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/checklist/${id}`)))
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklists excluídos com sucesso!')
      setModalVisivel(true)
    } catch {
      setErro('Erro ao excluir checklists')
    }
  }

  /**
   * Edita múltiplos checklists em massa via API
   * @param itensEditados Lista dos checklists editados
   */
  const handleEditarEmMassa = async (itensEditados: Checklist[]) => {
    setLoading(true)
    try {
      await Promise.all(
        itensEditados.map(item =>
          axios.put(`http://localhost:8000/api/checklist/${item.id}`, item)
        )
      )
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setEditaveis([])
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklists editados com sucesso!')
      setModalVisivel(true)
    } catch {
      setErro('Erro ao editar checklists em massa')
    } finally {
      setLoading(false)
    }
  }

  /**
   * Alterna seleção individual de checklist
   * @param id ID do checklist para toggle seleção
   */
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }

  /**
   * Alterna seleção de todos os checklists filtrados
   */
  const toggleSelecionarTodos = () => {
    if (todosSelecionados) {
      setSelecionados([])
    } else {
      setSelecionados(checklistsFiltrados.map(c => c.id))
    }
  }

  // Removido a função mostrarSelecao pois não está sendo utilizada

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Checklist</h1>

      <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Formulário de cadastro */}
        <ChecklistForm
          recebimentoId={recebimentoId}
          setRecebimentoId={setRecebimentoId}
          descricao={descricao}
          setDescricao={setDescricao}
          temPdf={temPdf}
          setTemPdf={setTemPdf}
          loading={loading}
          onSave={handleEnviar}
          recebimentosOptions={recebimentosOptions.map(String)}
        />

        {erro && (
        <div className="text-red-600 bg-red-100 border border-red-300 p-3 rounded-md">
          {erro}
        </div>
      )}
        {/* Filtros adicionais */}
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div>
            <label className="mr-2 font-medium">Filtro PDF:</label>
            <select
              className="border px-2 py-1 rounded"
              value={comPdfFilter}
              onChange={(e) => {
                setComPdfFilter(e.target.value as 'true' | 'false' | 'all')
                setPage(1) // Resetar página ao mudar filtro
              }}
            >
              <option value="all">Todos</option>
              <option value="true">Com PDF</option>
              <option value="false">Sem PDF</option>
            </select>
          </div>

          <div>
            <label className="mr-2 font-medium">Itens por página:</label>
            <select
              className="border px-2 py-1 rounded"
              value={limit}
              onChange={(e) => {
                setLimit(Number(e.target.value))
                setPage(1)
              }}
            >
              <option value={1}>1</option>
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
            </select>
          </div>
        </div>

        {/* Tabela de checklists */}
        <ChecklistTable
          checklists={checklistsFiltrados.map(item => ({
          ...item,
          recebimento_id: String(item.recebimento_id),
        }))}
          loading={loading || checklistsQuery.isLoading}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={todosSelecionados}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          setModoEdicaoMultipla={setModoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onSalvarEdicao={handleSalvarEdicao}
          onCancelarEdicao={handleCancelarEdicao}
          onDeleteEmMassa={excluirChecklistEmMassa}
          onEditarEmMassa={handleEditarEmMassa}
        />

        {/* Paginação */}
        <div className="flex flex-wrap items-center justify-center gap-2 mt-4">
          {/* Botão Anterior */}
          <button
            onClick={() => setPage(prev => Math.max(1, prev - 1))}
            disabled={page === 1}
            className={`flex items-center gap-1 px-3 py-1 rounded border transition
              ${page === 1 ? 'bg-gray-200 text-gray-400 cursor-not-allowed' : 'bg-white hover:bg-green-100 text-gray-800'}`}
          >
            <span>⬅️</span>
            <span>Anterior</span>
          </button>

          {/* Botões de página */}
          {checklistsQuery.data &&
            Array.from({ length: checklistsQuery.data.pages }, (_, i) => i + 1).map(num => (
              <button
                key={num}
                onClick={() => setPage(num)}
                className={`px-3 py-1 rounded border font-medium transition ${
                  num === page
                    ? 'bg-green-600 text-white'
                    : 'bg-white hover:bg-green-100 text-gray-700'
                }`}
              >
                {num}
              </button>
            ))}

          {/* Botão Próxima */}
          <button
            onClick={() =>
              setPage(prev => (checklistsQuery.data && prev < checklistsQuery.data.pages ? prev + 1 : prev))
            }
            disabled={checklistsQuery.data && page >= checklistsQuery.data.pages}
            className={`flex items-center gap-1 px-3 py-1 rounded border transition
              ${checklistsQuery.data && page >= checklistsQuery.data.pages
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-white hover:bg-green-100 text-gray-800'
              }`}
          >
            <span>Próxima</span>
            <span>➡️</span>
          </button>
        </div>

        {/* Modal de notificação */}
        <ModalNotificacao
          visivel={modalVisivel}
          onFechar={() => setModalVisivel(false)}
          titulo={tituloNotificacao}
          mensagem={mensagemNotificacao}
        />
      </div>
    </div>
  )
}
