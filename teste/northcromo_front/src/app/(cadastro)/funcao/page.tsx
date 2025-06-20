'use client'

import React, { useState } from 'react'
import axios from 'axios'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import FuncaoForm from '@/components/funcao/FuncaoForm'
import FuncaoTable from '@/components/funcao/FuncaoTable'
import ModalNotificacao from '@/components/ModalNotificacao'

interface Funcao {
  id: number
  funcao_nome: string
  data_cadastro: string
}

export default function FuncoesPage() {
  const [editando, setEditando] = useState<Funcao | null>(null)
  const queryClient = useQueryClient()
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')

  // Estado para seleção e edição na tabela
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [todosSelecionados, setTodosSelecionados] = useState(false)
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<number[]>([])

  // Busca funções
  const { data: funcoes = [], isLoading } = useQuery<Funcao[]>({
    queryKey: ['funcoes'],
    queryFn: async () => {
      const res = await axios.get('http://localhost:8000/api/funcoes')
      return res.data
    },
  })

  // Mutação para criar ou atualizar função
  const salvarFuncao = useMutation<
  void,
  unknown,
  { nome: string; dataCadastro: string; editando: Funcao | null }
>({
  mutationFn: async ({ nome, dataCadastro, editando }) => {
    if (editando) {
      await axios.put(`http://localhost:8000/api/funcoes/${editando.id}`, { funcao_nome: nome })
    } else {
      await axios.post('http://localhost:8000/api/funcoes', {
        funcao_nome: nome,
        data_cadastro: dataCadastro
      })
    }
  },
  onSuccess: () => {
    queryClient.invalidateQueries(['funcoes'])
    setEditando(null)
    setTituloNotificacao('Sucesso')
    setMensagemNotificacao('Função salva com sucesso!')
    setModalVisivel(true)
  },
  onError: () => {
    setTituloNotificacao('Erro')
    setMensagemNotificacao('Falha ao salvar função.')
    setModalVisivel(true)
  },
})

  // Mutação para deletar função
  const deletarFuncao = useMutation<void, unknown, number>({
    mutationFn: async (id: number) => {
      await axios.delete(`http://localhost:8000/api/funcoes/${id}`)
    },
    onSuccess: () => {
      queryClient.invalidateQueries(['funcoes'])
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Função deletada com sucesso!')
      setModalVisivel(true)
    },
    onError: () => {
      setTituloNotificacao('Erro')
      setMensagemNotificacao('Falha ao deletar função.')
      setModalVisivel(true)
    },
  })

  // Exemplos simples para as funções da tabela (implemente conforme necessário)
  function toggleSelecionado(id: number) {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }

  function toggleSelecionarTodos() {
    if (todosSelecionados) {
      setSelecionados([])
      setTodosSelecionados(false)
    } else {
      setSelecionados(funcoes.map(f => f.id))
      setTodosSelecionados(true)
    }
  }

  function onEdit(id: number) {
    const f = funcoes.find(f => f.id === id) || null
    setEditando(f)
  }

  function onDelete(id: number) {
    deletarFuncao.mutate(id)
  }

  function onSalvarEdicao(id: number, novoNome: string) {
    setEditando({ id, funcao_nome: novoNome })
    salvarFuncao.mutate(novoNome)
  }

  function onCancelarEdicao() {
    setEditando(null)
  }

  function onDeleteEmMassa(ids: number[]) {
    ids.forEach(id => deletarFuncao.mutate(id))
    setSelecionados([])
    setTodosSelecionados(false)
  }

  function onEditarEmMassa(ids: number[]) {
    // Implemente edição em massa se desejar
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white shadow rounded">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Funções</h1>

      <FuncaoForm
        funcaoId={editando?.id}
        nomeInicial={editando?.funcao_nome || ''}
        onSave={(nome, dataCadastro) => salvarFuncao.mutate({ nome,  dataCadastro,editando })}
        onCancel={() => setEditando(null)}
      />

      <FuncaoTable
        funcoes={funcoes}
        selecionados={selecionados}
        toggleSelecionado={toggleSelecionado}
        toggleSelecionarTodos={toggleSelecionarTodos}
        todosSelecionados={todosSelecionados}
        idEditar={idEditar}
        modoEdicaoMultipla={modoEdicaoMultipla}
        editaveis={editaveis}
        setEditaveis={setEditaveis}
        onEdit={onEdit}
        onDelete={onDelete}
        onSalvarEdicao={onSalvarEdicao}
        onCancelarEdicao={onCancelarEdicao}
        grupos={[]} // pode passar grupos/setores se quiser
        onDeleteEmMassa={onDeleteEmMassa}
        onEditarEmMassa={onEditarEmMassa}
      />

      <ModalNotificacao
        visivel={modalVisivel}
        onFechar={() => setModalVisivel(false)}
        titulo={tituloNotificacao}
        mensagem={mensagemNotificacao}
      />
    </div>
  )
}
