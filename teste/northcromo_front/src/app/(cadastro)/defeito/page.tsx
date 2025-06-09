'use client'
// src/app/(cadastro)/defeito/page.tsx
import React, { useState, useEffect } from 'react'
import ModalNotificacao from '@/components/ModalNotificacao'
import axios from 'axios'
import DefeitoTable from '@/components/defeito/DefeitoTable'
import useComponentesWS from '@/hooks/useComponentesWS'
import useDefeitoWS from '@/hooks/useDefeitoWS'

export interface Defeito {
  id?: number
  def_nome: string
  data: string
  componente_id: number
  componente_nome?: string
}

export default function DefeitoCadastro() {
  // Estados do formulário
  const [defNome, setDefNome] = useState('')
  const [dataDefeito, setDataDefeito] = useState('')
  const [componenteId, setComponenteId] = useState<number | ''>('')

  // Estados para a tabela
  const [defeitos, setDefeitos] = useState<Defeito[]>([])
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [editaveis, setEditaveis] = useState<Defeito[]>([])
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [todosSelecionados, setTodosSelecionados] = useState(false)

  // Modal notificação
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')

  // Loading e erro geral do form
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')

  // Usa hook para componentes
  const { componentesQuery } = useComponentesWS()

  // Usa hook para buscar defeitos (tanto via API quanto WebSocket)
  const { defeitosQuery } = useDefeitoWS()

  // Extrair dados e estados do query
  const componentes = componentesQuery.data ?? []
  const componentesLoading = componentesQuery.isLoading
  const componentesError =
    componentesQuery.error instanceof Error ? componentesQuery.error.message : null

  // Atualiza data default no carregamento
  useEffect(() => {
    setDataDefeito(new Date().toISOString().substring(0, 10));

    // Carregar defeitos assim que a página for carregada
  if (defeitosQuery.data) {
    setDefeitos(defeitosQuery.data);  // Atualiza o estado de defeitos com os dados carregados
  }
}, [defeitosQuery.data]);

  const handleEnviar = async () => {
    if (!defNome || !dataDefeito || !componenteId) {
      alert('Preencha todos os campos obrigatórios')
      return
    }

    setLoading(true)
    setErro('')

    const compSelecionado = componentes.find(c => c.id === Number(componenteId))
    const componenteNome = compSelecionado ? compSelecionado.componente_nome : ''

    const dados: Defeito = {
      def_nome: defNome,
      data: dataDefeito,
      componente_id: Number(componenteId),
      componente_nome: componenteNome,
    }

    try {
      const response = await axios.post('http://localhost:8000/api/defeito', dados)
      if (response.status === 200 || response.status === 201) {
        setTituloNotificacao('Sucesso')
        setMensagemNotificacao('Defeito cadastrado com sucesso!')
        setModalVisivel(true)

        // Adiciona o defeito ao estado local (de forma otimista)
        setDefeitos(prev => [...prev, response.data])

        // Resetar formulário
        setDefNome('')
        setDataDefeito(new Date().toISOString().substring(0, 10))
        setComponenteId('')
      } else {
        setErro('Erro ao salvar defeito')
      }
    } catch (error) {
      console.error('Erro ao salvar defeito:', error)
      setErro('Erro ao salvar defeito')
    } finally {
      setLoading(false)
    }
  }

  // Função para editar defeito
  const handleEdit = (defeito: Defeito) => {
    setIdEditar(defeito.id)
    setEditaveis([defeito])
  }

  // Função para excluir defeito
  const handleDelete = async (id: number) => {
    try {
      const response = await axios.delete(`http://localhost:8000/api/defeito/${id}`)
      if (response.status === 200) {
        setDefeitos(prev => prev.filter(d => d.id !== id))
        setTituloNotificacao('Sucesso')
        setMensagemNotificacao('Defeito excluído com sucesso!')
        setModalVisivel(true)
      } else {
        setErro('Erro ao excluir defeito')
      }
    } catch (error) {
      console.error('Erro ao excluir defeito:', error)
      setErro('Erro ao excluir defeito')
    }
  }

  // Função para salvar edição
  const handleSalvarEdicao = (itemEditado: Defeito) => {
    const novosDefeitos = defeitos.map(defeito =>
      defeito.id === itemEditado.id ? itemEditado : defeito
    )
    setDefeitos(novosDefeitos)
    setIdEditar(null)
    setEditaveis([])
  }

  // Função para cancelar edição
  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Defeito</h1>

      {/* Formulário de Cadastro */}
      <div className="bg-white p-6 rounded shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:space-x-4"> {/* Flex para controlar layout responsivo */}
          <div className="flex-1">
            <label className="block font-medium mb-1">Nome do Defeito</label>
            <input
              type="text"
              value={defNome}
              onChange={e => setDefNome(e.target.value.toUpperCase())}
              className="w-full border p-2 rounded"
              placeholder="Digite o nome do defeito"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Data do Defeito</label>
            <input
              type="date"
              value={dataDefeito}
              onChange={e => setDataDefeito(e.target.value)}
              className="w-full border p-2 rounded"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Componente</label>

            {componentesLoading && <p>Carregando componentes...</p>}
            {componentesError && <p className="text-red-500">{componentesError}</p>}

            {!componentesLoading && !componentesError && (
              <select
                value={componenteId}
                onChange={e => setComponenteId(Number(e.target.value))}
                className="w-full border p-2 rounded"
                disabled={loading}
              >
                <option value="">Selecione um componente</option>
                {componentes.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.componente_nome}
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>

        {erro && <p className="text-red-600">{erro}</p>}

        <button
          onClick={handleEnviar}
          disabled={loading || componentesLoading}
          className="w-full bg-green-700 text-white py-3 rounded font-semibold hover:bg-green-800 disabled:opacity-50"
        >
          {loading ? 'Enviando...' : 'Salvar Defeito'}
        </button>
      </div>

      {/* Exibição dos defeitos cadastrados */}
      <div className="mt-6">
        <DefeitoTable
          defeitos={defeitos}
          selecionados={selecionados}
          toggleSelecionado={(id) => setSelecionados(prev => prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id])}
          toggleSelecionarTodos={() => setTodosSelecionados(!todosSelecionados)}
          todosSelecionados={todosSelecionados}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onSalvarEdicao={handleSalvarEdicao}
          onCancelarEdicao={handleCancelarEdicao}
          componentes={componentes}
        />
      </div>

      {/* Modal Notificação */}
      <ModalNotificacao
        aberto={modalVisivel}
        onClose={() => setModalVisivel(false)}
        titulo={tituloNotificacao}
        mensagem={mensagemNotificacao}
      />
    </div>
  )
}
