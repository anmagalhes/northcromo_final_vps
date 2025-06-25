// src/app/(cadastro)/produto_tarefa/page.tsx
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

  // Estado que guarda a lista de tarefas carregadas da API
  const [listatarefa, setListatarefa] = useState<ProdutoTarefaItem[]>([])

  // REMOVIDO: loading e setLoading porque estavam definidos mas não usados.
  // Caso queira mostrar loading, descomente e utilize no JSX.
  // const [loading, setLoading] = useState(true)

  // Estados para edição de uma tarefa
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [nomeEditar, setNomeEditar] = useState('')

  // Estados para seleção múltipla e edição em lote
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)
  const [editaveis, setEditaveis] = useState<ProdutoTarefaItem[]>([])

  /**
   * useEffect que carrega a lista de tarefas do backend quando o componente monta.
   * Removeu o parâmetro de erro 'e' não usado no catch para evitar warnings do ESLint.
   */
  useEffect(() => {
    async function fetchtarefa() {
      // setLoading(true) removido por não uso

      try {
        const res = await fetch(`${baseURL}/produto_tarefa`)
        const data = await res.json()
        setListatarefa(data)
      } catch {
        alert('Erro ao carregar tarefa de trabalho')
      } finally {
        // setLoading(false) removido por não uso
      }
    }
    fetchtarefa()
  }, [])

  /**
   * Sincroniza os itens selecionados para edição múltipla.
   * Sempre que 'modoEdicaoMultipla', 'selecionados' ou 'listatarefa' mudam,
   * filtra os itens selecionados e os guarda em 'editaveis'.
   */
  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listatarefa.filter(p =>
        selecionados.includes(p.id)
      )
      setEditaveis(selecionadosEditaveis)
    }
  }, [modoEdicaoMultipla, selecionados, listatarefa])

  /**
   * Função que retorna uma string ISO 8601 com o horário ajustado para o fuso de São Paulo.
   * Essa função é usada para garantir que a data e hora estejam no horário local correto.
   */
  function getSaoPauloISOString(): string {
    const now = new Date()
    const formatter = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/Sao_Paulo',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    })

    const timeParts = Object.fromEntries(
      formatter.formatToParts(now).map(({ type, value }) => [type, value])
    )

    const ano = now.getFullYear()
    const mes = now.getMonth() + 1 // Mes começa de 0
    const dia = now.getDate()

    const dataSP = `${ano}-${String(mes).padStart(2, '0')}-${String(
      dia
    ).padStart(2, '0')}T${timeParts.hour}:${timeParts.minute}:${timeParts.second}`

    return dataSP // UTC com hora de SP aplicada
  }

  /**
   * Função para salvar uma nova tarefa ou editar uma existente.
   * Usa 'getSaoPauloISOString' para definir a data de execução corretamente.
   */
  const salvarTarefa = async (nome: string) => {
    const corpo = {
      produto_taf_nome: nome,
      data_execucao: getSaoPauloISOString(), // Corrigido para usar o horário de SP
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
        alert(idEditar ? 'Tarefa atualizada!' : 'Tarefa adicionada!')
        setIdEditar(null)
        setNomeEditar('')

        // Recarrega a lista após salvar para mostrar dados atualizados
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

  /**
   * Função para excluir uma tarefa pelo seu ID, após confirmação.
   * Atualiza os estados para remover o item da lista e da seleção.
   */
  const deletarTarefa = async (id: number) => {
    if (!confirm('Deseja realmente excluir este Tarefa de trabalho?')) return

    try {
      await fetch(`${baseURL}/produto_tarefa/${id}`, { method: 'DELETE' })
      alert('Tarefa excluída.')
      setSelecionados(prev => prev.filter(x => x !== id))
      setListatarefa(prev => prev.filter(p => p.id !== id))
    } catch {
      alert('Erro ao excluir.')
    }
  }

  /**
   * Função para excluir várias tarefas selecionadas em lote, após confirmação.
   */
  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhuma tarefa selecionada.')
      return
    }

    if (!confirm(`Deseja excluir ${selecionados.length} tarefa(s)?`)) return

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/produto_tarefa/${id}`, { method: 'DELETE' })
      }
      alert('Tarefas selecionadas excluídas com sucesso.')
      setSelecionados([])
      setListatarefa(prev => prev.filter(p => !selecionados.includes(p.id)))
    } catch {
      alert('Erro ao excluir tarefas.')
    }
  }

  /**
   * Atualiza múltiplas tarefas em lote.
   * Envia uma requisição PUT para cada item editável e atualiza a lista.
   */
  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/produto_tarefa/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        })
      }
      alert('Tarefas atualizadas com sucesso.')
      setModoEdicaoMultipla(false)
      setSelecionados([])
      setEditaveis([])

      // Recarrega a lista atualizada
      const res2 = await fetch(`${baseURL}/produto_tarefa`)
      const updatedList = await res2.json()
      setListatarefa(updatedList)
    } catch {
      alert('Erro ao atualizar tarefas.')
    }
  }

  /**
   * Começa edição de um item individual, setando estados para o formulário.
   */
  const editarTarefa = (item: ProdutoTarefaItem) => {
    setIdEditar(item.id)
    setNomeEditar(item.produto_taf_nome)
  }

  /**
   * Cancela a edição atual, limpando os estados de edição.
   */
  const cancelarEdicao = () => {
    setIdEditar(null)
    setNomeEditar('')
  }

  /**
   * Alterna a seleção de um item na lista.
   * Se já está selecionado, remove da seleção, senão adiciona.
   */
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    )
  }

  /**
   * Seleciona todos os itens da lista ou limpa a seleção caso todos já estejam selecionados.
   */
  const toggleSelecionarTodos = () => {
    if (selecionados.length === listatarefa.length) {
      setSelecionados([])
    } else {
      setSelecionados(listatarefa.map(item => item.id))
    }
  }

  /**
   * Salva a edição de um item individual da lista.
   * Atualiza localmente a lista e avisa o usuário.
   */
  const salvarEdicao = async (itemEditado: ProdutoTarefaItem) => {
    try {
      const res = await fetch(`${baseURL}/produto_tarefa/${itemEditado.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(itemEditado),
      })
      if (!res.ok) {
        const data = await res.json()
        alert(data.detail || 'Erro ao salvar edição.')
      } else {
        alert('Tarefa atualizada com sucesso.')
        // Atualiza localmente a lista para refletir a edição
        setListatarefa(prev =>
          prev.map(p => (p.id === itemEditado.id ? itemEditado : p))
        )
      }
    } catch {
      alert('Erro de conexão ao salvar edição.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 px-4 sm:px-6 md:px-12 py-8">
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro de tarefa de Trabalho
        </h1>

        {/* Formulário para adicionar/editar tarefa */}
        <Produto_TarefaForm
          tarefaId={idEditar ? String(idEditar) : undefined}
          tarefaNome={nomeEditar}
          onSave={salvarTarefa}
          onCancel={idEditar ? cancelarEdicao : undefined}
        />

        {/* Botões para edição múltipla ou exclusão quando há seleções */}
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

        {/* Tabela que exibe as tarefas com suporte a edição e seleção múltipla */}
        <Produto_TarefaTable
          tarefa={listatarefa}
          onEdit={editarTarefa}
          onDelete={deletarTarefa}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={
            selecionados.length === listatarefa.length && listatarefa.length > 0
          }
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onSalvarMultiplos={atualizarEmLote} // salvar em lote
          onCancelarMultiplos={() => {
            setModoEdicaoMultipla(false)
            setEditaveis([])
          }}
          onSalvarEdicao={salvarEdicao} // salvar item individual
        />
      </div>
    </div>
  )
}
