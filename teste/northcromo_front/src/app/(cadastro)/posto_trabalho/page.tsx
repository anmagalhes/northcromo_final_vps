// src/app/posto_trabalho/page.tsx
'use client';

import React, { useState, useEffect } from 'react'
import PostoTrabalhoForm from '@/components/posto_trabalho/Posto_TrabalhoForm'
import PostoTrabalhoTable from '@/components/posto_trabalho/Posto_TrabalhoTable'

interface PostoTrabalhoItem {
  id: number
  posto_trabalho_nome: string
  data_execucao: string
}

export default function PostoTrabalhoPage() {
  const baseURL = 'http://localhost:8000/api'

  // Aqui você precisaria trocar para seu hook ou fetch dos postos trabalho
  const [listaPostos, setListaPostos] = useState<PostoTrabalhoItem[]>([])
  const [loading, setLoading] = useState(true)

  // Estados de edição
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [nomeEditar, setNomeEditar] = useState('')
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<PostoTrabalhoItem[]>([])

  // Carrega lista de postos
  useEffect(() => {
    async function fetchPostos() {
      setLoading(true)
      try {
        const res = await fetch(`${baseURL}/posto_trabalho`)
        const data = await res.json()
        setListaPostos(data)
      } catch (e) {
        alert('Erro ao carregar postos de trabalho')
      } finally {
        setLoading(false)
      }
    }
    fetchPostos()
  }, [])

  // Sincroniza itens editáveis para edição múltipla
  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listaPostos.filter(p =>
        selecionados.includes(p.id)
      )
      setEditaveis(selecionadosEditaveis)
    }
  }, [modoEdicaoMultipla, selecionados, listaPostos])

  // Salvar novo ou editar existente
  const salvarPosto = async (nome: string) => {
    const corpo = {
      posto_trabalho_nome: nome,
      data_execucao: new Date().toISOString(),
    }

    try {
      const metodo = idEditar ? 'PUT' : 'POST'
      const url = idEditar
        ? `${baseURL}/posto_trabalho/${idEditar}`
        : `${baseURL}/posto_trabalho`

      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      })

      const data = await res.json()

      if (res.ok) {
        alert(idEditar ? 'Posto atualizado!' : 'Posto adicionado!')
        setIdEditar(null)
        setNomeEditar('')
        // Recarregar lista após salvar
        const res2 = await fetch(`${baseURL}/posto_trabalho`)
        const updatedList = await res2.json()
        setListaPostos(updatedList)
      } else {
        alert(data.detail || 'Erro ao salvar.')
      }
    } catch {
      alert('Erro de conexão.')
    }
  }

  // Excluir um posto
  const deletarPosto = async (id: number) => {
    if (!confirm('Deseja realmente excluir este posto de trabalho?')) return

    try {
      await fetch(`${baseURL}/posto_trabalho/${id}`, { method: 'DELETE' })
      alert('Posto excluído.')
      setSelecionados(prev => prev.filter(x => x !== id))
      setListaPostos(prev => prev.filter(p => p.id !== id))
    } catch {
      alert('Erro ao excluir.')
    }
  }

  // Excluir selecionados
  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhum posto selecionado.')
      return
    }

    if (!confirm(`Deseja excluir ${selecionados.length} posto(s)?`)) return

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/posto_trabalho/${id}`, { method: 'DELETE' })
      }
      alert('Postos selecionados excluídos com sucesso.')
      setSelecionados([])
      setListaPostos(prev => prev.filter(p => !selecionados.includes(p.id)))
    } catch {
      alert('Erro ao excluir postos.')
    }
  }


  // Atualizar múltiplos em lote
  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/posto_trabalho/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        })
      }
      alert('Postos atualizados com sucesso.')
      setModoEdicaoMultipla(false)
      setSelecionados([])
      setEditaveis([])

      // Recarregar lista
      const res2 = await fetch(`${baseURL}/posto_trabalho`)
      const updatedList = await res2.json()
      setListaPostos(updatedList)
    } catch {
      alert('Erro ao atualizar postos.')
    }
  }

  // Começar edição de um posto
  const editarPosto = (item: PostoTrabalhoItem) => {
    setIdEditar(item.id)
    setNomeEditar(item.posto_trabalho_nome)
  }

  // Cancelar edição
  const cancelarEdicao = () => {
    setIdEditar(null)
    setNomeEditar('')
  }

  // Alternar seleção
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

  // Selecionar todos ou limpar seleção
  const toggleSelecionarTodos = () => {
    if (selecionados.length === listaPostos.length) {
      setSelecionados([])
    } else {
      setSelecionados(listaPostos.map(item => item.id))
    }
  }

  const salvarEdicao = async (itemEditado: PostoTrabalhoItem) => {
    try {
      const res = await fetch(`${baseURL}/posto_trabalho/${itemEditado.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemEditado),
      });
      if (!res.ok) {
        const data = await res.json();
        alert(data.detail || 'Erro ao salvar edição.');
      } else {
        alert('Posto atualizado com sucesso.');
        // Atualiza localmente a lista
        setListaPostos(prev =>
          prev.map(p => (p.id === itemEditado.id ? itemEditado : p))
        );
      }
    } catch {
      alert('Erro de conexão ao salvar edição.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 px-4 sm:px-6 md:px-12 py-8">
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro de Postos de Trabalho
        </h1>

        <PostoTrabalhoForm
          postoId={idEditar ? String(idEditar) : undefined}
          postoNome={nomeEditar}
          onSave={salvarPosto}
          onCancel={idEditar ? cancelarEdicao : undefined}
        />

        {selecionados.length > 0 && !modoEdicaoMultipla && (
          <div className="mb-4 flex justify-end gap-3">
            <button
              onClick={() => setModoEdicaoMultipla(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Editar Selecionados ({selecionados.length})
            </button>
            <button
              onClick={deletarSelecionados}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
            >
              Excluir Selecionados ({selecionados.length})
            </button>
          </div>
        )}

        <PostoTrabalhoTable
          postos={listaPostos}
          onEdit={editarPosto}
          onDelete={deletarPosto}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={selecionados.length === listaPostos.length && listaPostos.length > 0}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onSalvarMultiplos={atualizarEmLote} // ✅ salvar em lote
          onCancelarMultiplos={() => {
            setModoEdicaoMultipla(false)
            setEditaveis([])
          }}
          onSalvarEdicao={salvarEdicao} // ✅ salvar item individual
        />
      </div>
    </div>
  )
}
