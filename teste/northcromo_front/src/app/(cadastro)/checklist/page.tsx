// src/app/checklis/page.tsx

'use client'
import React, { useState, useEffect } from 'react'
import ChecklistForm from '@/components/checklist/ChecklistForm'
import ChecklistTable from '@/components/checklist/ChecklistTable'
import ModalNotificacao from '@/components/ModalNotificacao'
import useChecklistWS, { Checklist } from '@/hooks/useChecklistWS'
import axios from 'axios'

export default function ChecklistPage() {

  // Paginação e filtros gerais
  const [page, setPage] = useState(1)
  const [limit, setLimit] = useState(20)
  const [comPdfFilter, setComPdfFilter] = useState<'true' | 'false' | 'all'>('all')

  // Hook customizado para buscar os checklists
  const { checklistsQuery } = useChecklistWS(page, limit, comPdfFilter)
  const checklists = checklistsQuery.data?.data || []

  // Formulário para cadastro de checklist
  const [recebimentoId, setRecebimentoId] = useState('')
  const [descricao, setDescricao] = useState('')
  const [temPdf, setTemPdf] = useState(false)

  // Estado para filtro de recebimento separado do formulário
  const [filtroRecebimentoId, setFiltroRecebimentoId] = useState<string | null>(null)

  // Notificações e erros
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [erro, setErro] = useState('')

  // Seleção e edição
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<Checklist[]>([])
  const [loading, setLoading] = useState(false)

  // Extrair IDs únicos de recebimento para filtro (sem duplicatas)
  const recebimentosOptions = Array.from(new Set(checklists.map(c => c.recebimento_id)))

  // Filtrar a lista conforme o recebimentoId digitado no formulário (se tiver valor)
  const checklistsFiltrados = recebimentoId
  ? checklists.filter(c => c.recebimento_id === recebimentoId)
  : checklists

  // Verifica se todos os filtrados estão selecionados
  const todosSelecionados = selecionados.length === checklistsFiltrados.length && checklistsFiltrados.length > 0

  // Limpa os campos do formulário
  const limparCampos = () => {
    setRecebimentoId('')
    setDescricao('')
    setTemPdf(false)
    setErro('')
  }

  // Cadastra novo checklist
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
    } catch (error) {
      console.error('Erro ao cadastrar checklist:', error)
      setErro('Erro ao salvar checklist')
    } finally {
      setLoading(false)
    }
  }

  // Edita checklist individual
  const handleEdit = (item: Checklist) => {
    setIdEditar(item.id)
    setEditaveis([item])
    setModoEdicaoMultipla(false)
    setSelecionados([])
  }

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

  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
  }

  // Delete checklist individual
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

  // Excluir múltiplos checklists
  const excluirChecklistEmMassa = async (ids: number[]) => {
    try {
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/checklist/${id}`)))
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Checklists excluídos com sucesso!')
      setModalVisivel(true)
    } catch (error) {
      setErro('Erro ao excluir checklists')
    }
  }

  // Editar múltiplos checklists
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
    } catch (error) {
      setErro('Erro ao editar checklists em massa')
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

  // Toggle selecionar todos visíveis no filtro atual
  const toggleSelecionarTodos = () => {
    if (todosSelecionados) {
      setSelecionados([])
    } else {
      setSelecionados(checklistsFiltrados.map(c => c.id))
    }
  }

  // Função para abrir o modal com a seleção atual
const mostrarSelecao = () => {
  if (selecionados.length === 0) {
    setTituloNotificacao('Nenhuma seleção');
    setMensagemNotificacao('Nenhum item está selecionado.');
  } else {
    setTituloNotificacao('Seleção atualizada');
    setMensagemNotificacao(`Você selecionou ${selecionados.length} item(s).`);
  }
  setModalVisivel(true);
};


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
          erro={erro}
          recebimentosOptions={recebimentosOptions}
        />

        {/* Filtros adicionais */}
        <div className="flex flex-wrap gap-4 items-center justify-between">
          <div>
            <label className="mr-2 font-medium">Filtro PDF:</label>
            <select
              className="border px-2 py-1 rounded"
              value={comPdfFilter}
              onChange={(e) => {
                setComPdfFilter(e.target.value as 'true' | 'false' | 'all')
                setPage(1) // Reset página ao mudar filtro
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
          checklists={checklistsFiltrados}
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
