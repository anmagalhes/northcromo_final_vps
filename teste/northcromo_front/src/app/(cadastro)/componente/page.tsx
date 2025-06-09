'use client'
//src/app/(cadastro)/componente/pag.tsx
import React, { useState, useEffect, useMemo } from 'react'
import ComponenteForm from '@/components/componente/ComponenteForm'
import ComponenteTable from '@/components/componente/ComponenteTable'
import useComponentesWS from '@/hooks/useComponentesWS'

interface ComponenteItem {
  id: number
  componente_nome: string
  data_recebimento: string
}

export default function ComponentePage() {
  const { componentesQuery } = useComponentesWS()
  const listaComponentesRaw = componentesQuery.data || []
  // Memoiza para evitar re-execução desnecessária no useEffect
  const listaComponentes = useMemo(() => listaComponentesRaw, [listaComponentesRaw])

  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [nomeEditar, setNomeEditar] = useState('')
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<ComponenteItem[]>([])

  const baseURL = 'http://localhost:8000/api'

  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listaComponentes.filter(c => selecionados.includes(c.id))
      setEditaveis(selecionadosEditaveis)
    }
  }, [modoEdicaoMultipla, selecionados, listaComponentes])

  const salvarComponente = async (nome: string) => {
    const corpo = {
      componente_nome: nome,
      data_recebimento: new Date().toISOString(),
    }

    try {
      const metodo = idEditar ? 'PUT' : 'POST'
      const url = idEditar
        ? `${baseURL}/componente/${idEditar}`
        : `${baseURL}/componente`

      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      })

      const data = await res.json()

      if (res.ok) {
        alert(idEditar ? 'Componente atualizado!' : 'Componente adicionado!')
        setIdEditar(null)
        setNomeEditar('')
      } else {
        alert(data.detail || 'Erro ao salvar.')
      }
    } catch {
      alert('Erro de conexão.')
    }
  }

  const deletarComponente = async (id: number) => {
    if (!confirm('Deseja realmente excluir este componente?')) return

    try {
      await fetch(`${baseURL}/componente/${id}`, { method: 'DELETE' })
      alert('Componente excluído.')
      setSelecionados((prev) => prev.filter(x => x !== id))
    } catch {
      alert('Erro ao excluir.')
    }
  }

  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhum componente selecionado.')
      return
    }

    if (!confirm(`Deseja excluir ${selecionados.length} componente(s)?`)) return

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/componente/${id}`, { method: 'DELETE' })
      }
      alert('Componentes selecionados excluídos com sucesso.')
      setSelecionados([])
    } catch {
      alert('Erro ao excluir componentes selecionados.')
    }
  }

  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/componente/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        })
      }
      alert('Componentes atualizados com sucesso.')
      setModoEdicaoMultipla(false)
      setSelecionados([])
      setEditaveis([])
    } catch {
      alert('Erro ao atualizar componentes.')
    }
  }

  const editarComponente = (item: ComponenteItem) => {
    setIdEditar(item.id)
    setNomeEditar(item.componente_nome)
  }

  const cancelarEdicao = () => {
    setIdEditar(null)
    setNomeEditar('')
  }

  const toggleSelecionado = (id: number) => {
    setSelecionados((prev) =>
      prev.includes(id) ? prev.filter((x) => x !== id) : [...prev, id]
    )
  }

  const toggleSelecionarTodos = () => {
    if (selecionados.length === listaComponentes.length) {
      setSelecionados([])
    } else {
      setSelecionados(listaComponentes.map((item) => item.id))
    }
  }

  const salvarEdicao = async (itemEditado: ComponenteItem) => {
    try {
      const res = await fetch(`${baseURL}/componente/${itemEditado.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemEditado),
      })
      if (!res.ok) {
        const data = await res.json()
        alert(data.detail || 'Erro ao salvar edição.')
      } else {
        alert('Componente atualizado automaticamente.')
      }
    } catch {
      alert('Erro de conexão ao salvar edição.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 px-4 sm:px-6 md:px-12 py-8">
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro Componentes
        </h1>

        <ComponenteForm
          componenteId={idEditar ? String(idEditar) : undefined}
          componenteNome={nomeEditar}
          onSave={salvarComponente}
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

        <ComponenteTable
          componentes={listaComponentes}
          onEdit={editarComponente}
          onDelete={deletarComponente}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={selecionados.length === listaComponentes.length}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onSalvarMultiplos={atualizarEmLote}
          onCancelarMultiplos={() => {
            setModoEdicaoMultipla(false)
            setEditaveis([])
          }}
          onSalvarEdicao={salvarEdicao}
        />
      </div>
    </div>
  )
}
