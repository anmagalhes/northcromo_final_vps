// src/app/Produto_Tarefa/page.tsx
'use client';

import React, { useState, useEffect } from 'react'
import Produto_TarefaForm from '@/components/produto_tarefa/Produto_TarefaForm'
import Produto_TarefaTable from '@/components/produto_tarefa/Produto_TarefaTable'

interface ProdutoTarefaItem {
  id: number
  produto_taf_nome: string
  data_execucao: string
}

export default function Produto_TarefaPage() {
  const baseURL = 'http://localhost:8000/api'

  // Aqui você precisaria trocar para seu hook ou fetch dos tarefa trabalho
  const [listatarefa, setListatarefa] = useState<ProdutoTarefaItem[]>([])
  const [loading, setLoading] = useState(true)

  // Estados de edição
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [nomeEditar, setNomeEditar] = useState('')
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<ProdutoTarefaItem[]>([])


  // Carrega lista de tarefa
  useEffect(() => {
    async function fetchtarefa() {
      setLoading(true)
      try {
        const res = await fetch(`${baseURL}/produto_tarefa`)
        const data = await res.json()
        setListatarefa(data)
      } catch (e) {
        alert('Erro ao carregar tarefa de trabalho')
      } finally {
        setLoading(false)
      }
    }
    fetchtarefa()
  }, [])

  // Sincroniza itens editáveis para edição múltipla
  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listatarefa.filter(p =>
        selecionados.includes(p.id)
      )
      setEditaveis(selecionadosEditaveis)
    }
  }, [modoEdicaoMultipla, selecionados, listatarefa])



function getSaoPauloISOString(): string {
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Sao_Paulo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });

  const timeParts = Object.fromEntries(
    formatter.formatToParts(now).map(({ type, value }) => [type, value])
  );

  const ano = now.getFullYear();
  const mes = now.getMonth() + 1; // Mes começa de 0
  const dia = now.getDate();

  const dataSP = `${ano}-${String(mes).padStart(2, '0')}-${String(dia).padStart(2, '0')}T${timeParts.hour}:${timeParts.minute}:${timeParts.second}`;

  return dataSP; // UTC com hora de SP aplicada
}

  // Salvar novo ou editar existente
  const salvarTarefa = async (nome: string) => {
    const corpo = {
      produto_taf_nome: nome,
      data_execucao: new Date().toISOString(),
    }

    try {
      const metodo = idEditar ? 'PUT' : 'POST'
      const url = idEditar
        ? `${baseURL}/produto_tarefa/${idEditar}`
        : `${baseURL}/produto_tarefa`

      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      })

      const data = await res.json()

      if (res.ok) {
        alert(idEditar ? 'Tarefa atualizado!' : 'Tarefa adicionado!')
        setIdEditar(null)
        setNomeEditar('')

        // Recarregar lista após salvar
        const res2 = await fetch(`${baseURL}/produto_tarefa`)
        const updatedList = await res2.json()
        setListatarefa(updatedList)
      } else {
        alert(data.detail || 'Erro ao salvar.')
      }
    } catch {
      alert('Erro de conexão.')
    }
  }

  // Excluir um Tarefa
  const deletarTarefa = async (id: number) => {
    if (!confirm('Deseja realmente excluir este Tarefa de trabalho?')) return

    try {
      await fetch(`${baseURL}/produto_tarefa/${id}`, { method: 'DELETE' })
      alert('Tarefa excluído.')
      setSelecionados(prev => prev.filter(x => x !== id))
      setListatarefa(prev => prev.filter(p => p.id !== id))
    } catch {
      alert('Erro ao excluir.')
    }
  }

  // Excluir selecionados
  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhum Tarefa selecionado.')
      return
    }

    if (!confirm(`Deseja excluir ${selecionados.length} Tarefa(s)?`)) return

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/produto_tarefa/${id}`, { method: 'DELETE' })
      }
      alert('tarefa selecionados excluídos com sucesso.')
      setSelecionados([])
      setListatarefa(prev => prev.filter(p => !selecionados.includes(p.id)))
    } catch {
      alert('Erro ao excluir tarefa.')
    }
  }


  // Atualizar múltiplos em lote
  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/produto_tarefa/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        })
      }
      alert('tarefa atualizados com sucesso.')
      setModoEdicaoMultipla(false)
      setSelecionados([])
      setEditaveis([])

      // Recarregar lista
      const res2 = await fetch(`${baseURL}/produto_tarefa`)
      const updatedList = await res2.json()
      setListatarefa(updatedList)
    } catch {
      alert('Erro ao atualizar tarefa.')
    }
  }

  // Começar edição de um Tarefa
  const editarTarefa = (item: ProdutoTarefaItem) => {
    setIdEditar(item.id)
    setNomeEditar(item.produto_taf_nome)
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
    if (selecionados.length === listatarefa.length) {
      setSelecionados([])
    } else {
      setSelecionados(listatarefa.map(item => item.id))
    }
  }

  const salvarEdicao = async (itemEditado: ProdutoTarefaItem) => {
    try {
      const res = await fetch(`${baseURL}/produto_tarefa/${itemEditado.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemEditado),
      });
      if (!res.ok) {
        const data = await res.json();
        alert(data.detail || 'Erro ao salvar edição.');
      } else {
        alert('Tarefa atualizado com sucesso.');
        // Atualiza localmente a lista
        setListatarefa(prev =>
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
          Cadastro de tarefa de Trabalho
        </h1>

        <Produto_TarefaForm
          TarefaId={idEditar ? String(idEditar) : undefined}
          TarefaNome={nomeEditar}
          onSave={salvarTarefa}
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

        <Produto_TarefaTable
          tarefa={listatarefa}
          onEdit={editarTarefa}
          onDelete={deletarTarefa}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={selecionados.length === listatarefa.length && listatarefa.length > 0}
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
