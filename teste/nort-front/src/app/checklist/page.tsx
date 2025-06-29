// src/app/checklist/page.tsx
'use client'

import React, { useState, useMemo } from 'react'
import ChecklistForm from '@/components/checklist/ChecklistForm'
import ChecklistTable from '@/components/checklist/ChecklistTable'
import ModalNotificacao from '@/components/ModalNotificacao'
import { Checklist } from '@/types/checklist'
import useChecklistWS from '@/hooks/useChecklistWS'
import axios from 'axios'

import 'react-datepicker/dist/react-datepicker.css'

export default function ChecklistPage() {

  // Paginação e filtros
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(20)
  const [comPdfFilter, setComPdfFilter] = useState<'true' | 'false' | 'all'>('all')

  // Filtro específico para recebimento separado do formulário
  const [recebimentoIdFilter, setRecebimentoIdFilter] = useState<string>('')

  // Hook customizado para dados
  const { checklistsQuery } = useChecklistWS(page, limit, comPdfFilter)
  const checklists = useMemo(() => checklistsQuery.data?.data || [], [checklistsQuery.data])

  // Estados do formulário
  const [recebimentoIdForm, setRecebimentoIdForm] = useState<string>('')
  const [descricao, setDescricao] = useState('')
  const [temPdf, setTemPdf] = useState(false)

  // Notificações e erro
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [erro, setErro] = useState<string>('')

  // Seleção e edição
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<Checklist[]>([])
  const [loading, setLoading] = useState(false)

  // Opções únicas para filtro, string padronizado
  const recebimentosOptions = useMemo(
    () =>
      Array.from(
        new Set(checklists.map(c => String(c.recebimento_id)))
      ),
    [checklists]
  )

  // Filtra checklists pelo recebimentoIdFilter
  const checklistsFiltrados = useMemo(() => {
    if (recebimentoIdFilter) {
      return checklists.filter(c => String(c.recebimento_id) === recebimentoIdFilter)
    }
    return checklists
  }, [checklists, recebimentoIdFilter])

  // Verifica seleção total
  const todosSelecionados =
    selecionados.length === checklistsFiltrados.length && checklistsFiltrados.length > 0


  // Limpa formulário e erros
  const limparCampos = () => {
    setRecebimentoIdForm('')
    setDescricao('')
    setTemPdf(false)
    setErro('')
  }

  // Função para mostrar notificação
  const mostrarNotificacao = (titulo: string, mensagem: string) => {
    setTituloNotificacao(titulo)
    setMensagemNotificacao(mensagem)
    setModalVisivel(true)
  }

  // Handler para cadastro
  const handleEnviar = async () => {
    if (!recebimentoIdForm || !descricao) {
      setErro('Preencha todos os campos')
      return
    }
    setLoading(true)
    setErro('')
    try {
      await axios.post('http://localhost:8000/api/checklist', {
        recebimento_id: recebimentoIdForm,
        descricao,
        tem_pdf: temPdf,
      })
      limparCampos()
      mostrarNotificacao('Sucesso', 'Checklist cadastrado com sucesso!')
    } catch (err: unknown) {
  if (axios.isAxiosError(err)) {
    setErro(err.response?.data?.message || 'Erro ao salvar checklist')
      } else {
        setErro('Erro inesperado')
      }
    } finally {
      setLoading(false)
    }
  }

  // Iniciar edição individual
  const handleEdit = (item: Checklist) => {
    setIdEditar(item.id)
    setEditaveis([item])
    setModoEdicaoMultipla(false)
    setSelecionados([])
    setErro('')
  }

  // Salvar edição individual
  const handleSalvarEdicao = async (editado: Checklist) => {
    setLoading(true)
    setErro('')
    try {
      await axios.put(`http://localhost:8000/api/checklist/${editado.id}`, editado)
      setIdEditar(null)
      setEditaveis([])
      mostrarNotificacao('Sucesso', 'Checklist editado com sucesso!')
    } catch (err: unknown) {
      if (axios.isAxiosError(err)) {
        setErro(err.response?.data?.message || 'Erro ao salvar edição')
      } else {
        setErro('Erro inesperado')
      }
    } finally {
      setLoading(false)
    }
 }


  // Cancelar edição
  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
    setErro('')
  }

  // Excluir individual
  const handleDelete = async (id: number) => {
    setErro('')
    try {
      await axios.delete(`http://localhost:8000/api/checklist/${id}`)
      mostrarNotificacao('Sucesso', 'Checklist excluído com sucesso!')
    } catch (err: unknown) {
    if (axios.isAxiosError(err)) {
      setErro(err.response?.data?.message || 'Erro ao excluir checklist')
    } else {
      setErro('Erro inesperado')
    }
  }
  }


  // Excluir múltiplos
  const excluirChecklistEmMassa = async (ids: number[]) => {
    setErro('')
    try {
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/checklist/${id}`)))
      setSelecionados([])
      setModoEdicaoMultipla(false)
      mostrarNotificacao('Sucesso', 'Checklists excluídos com sucesso!')
    } catch (err: unknown) {
  if (axios.isAxiosError(err)) {
    setErro(err.response?.data?.message || 'Erro ao excluir checklists')
  } else {
    setErro('Erro inesperado')
  }
}
}

  // Editar múltiplos em massa
  const handleEditarEmMassa = async (itensEditados: Checklist[]) => {
    setLoading(true)
    setErro('')
    try {
      await Promise.all(
        itensEditados.map(item =>
          axios.put(`http://localhost:8000/api/checklist/${item.id}`, item)
        )
      )
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setEditaveis([])
      mostrarNotificacao('Sucesso', 'Checklists editados com sucesso!')
   } catch (err: unknown) {
  if (axios.isAxiosError(err)) {
    setErro(err.response?.data?.message || 'Erro ao editar checklists em massa')
  } else {
    setErro('Erro inesperado')
  }
} finally {
  setLoading(false)
}
}


  // Toggle seleção individual
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }

  // Toggle seleção todos
  const toggleSelecionarTodos = () => {
    if (todosSelecionados) {
      setSelecionados([])
    } else {
      setSelecionados(checklistsFiltrados.map(c => c.id))
    }
  }

  // Função para mudar filtro PDF, limpa erro e reseta página
  const handleComPdfFilterChange = (value: 'true' | 'false' | 'all') => {
    setComPdfFilter(value)
    setPage(1)
    setErro('')
  }

  // Função para mudar itens por página
  const handleLimitChange = (value: number) => {
    setLimit(value)
    setPage(1)
    setErro('')
  }

  // Função para mudar filtro recebimento
  const handleRecebimentoFilterChange = (value: string) => {
    setRecebimentoIdFilter(value)
    setPage(1)
    setErro('')
  }

  // Paginação: limitar a exibição de botões para até 7
  const renderPageButtons = () => {
    if (!checklistsQuery.data) return null

    const totalPages = checklistsQuery.data.pages
    const maxButtons = 7
    let startPage = Math.max(page - 3, 1)
    const endPage = Math.min(startPage + maxButtons - 1, totalPages)

    if (endPage - startPage < maxButtons - 1) {
      startPage = Math.max(endPage - maxButtons + 1, 1)
    }

    const buttons = []
    for (let num = startPage; num <= endPage; num++) {
      buttons.push(
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
      )
    }
    return buttons
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Checklist</h1>

      <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
        {/* Formulário */}
        <ChecklistForm
          recebimentoId={recebimentoIdForm}
          setRecebimentoId={setRecebimentoIdForm}
          //descricao={descricao}
         // setDescricao={setDescricao}
         // temPdf={temPdf}
          //setTemPdf={setTemPdf}
          loading={loading}
          onSave={handleEnviar}
          recebimentosOptions={recebimentosOptions}
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
              onChange={e => handleComPdfFilterChange(e.target.value as 'true' | 'false' | 'all')}
            >
              <option value="all">Todos</option>
              <option value="true">Com PDF</option>
              <option value="false">Sem PDF</option>
            </select>
          </div>

          <div>
            <label className="mr-2 font-medium">Filtro Recebimento:</label>
            <select
              className="border px-2 py-1 rounded"
              value={recebimentoIdFilter}
              onChange={e => handleRecebimentoFilterChange(e.target.value)}
            >
              <option value="">Todos</option>
              {recebimentosOptions.map(id => (
                <option key={id} value={id}>
                  {id}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="mr-2 font-medium">Itens por página:</label>
            <select
              className="border px-2 py-1 rounded"
              value={limit}
              onChange={e => handleLimitChange(Number(e.target.value))}
            >
              <option value={1}>1</option>
              <option value={5}>5</option>
              <option value={10}>10</option>
              <option value={20}>20</option>
            </select>
          </div>
        </div>

        {/* Tabela */}
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
          <button
            onClick={() => setPage(prev => Math.max(1, prev - 1))}
            disabled={page === 1}
            className={`flex items-center gap-1 px-3 py-1 rounded border transition ${
              page === 1
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-white hover:bg-green-100 text-gray-800'
            }`}
          >
            <span>⬅️</span>
            <span>Anterior</span>
          </button>

          {renderPageButtons()}

          <button
            onClick={() =>
              setPage(prev =>
                checklistsQuery.data && prev < checklistsQuery.data.pages ? prev + 1 : prev
              )
            }
            disabled={checklistsQuery.data && page >= checklistsQuery.data.pages}
            className={`flex items-center gap-1 px-3 py-1 rounded border transition ${
              checklistsQuery.data && page >= checklistsQuery.data.pages
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-white hover:bg-green-100 text-gray-800'
            }`}
          >
            <span>Próxima</span>
            <span>➡️</span>
          </button>
        </div>

        {/* Modal */}
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
