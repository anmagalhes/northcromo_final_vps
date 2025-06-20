// src/components/produto_tarefa/ProdutoTarefaForm.tsx
import React, { useState, useEffect } from 'react'

interface Props {
  tarefaId?: string
  tarefaNome?: string
  onSave: (nome: string, dataExecucao: string, id?: string) => void
  onCancel?: () => void
}

export default function ProdutoTarefaForm({
  tarefaId,
  tarefaNome = '',
  onSave,
  onCancel,
}: Props) {
  const [nome, setNome] = useState(tarefaNome)

  useEffect(() => {
    setNome(tarefaNome)
  }, [tarefaNome])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nome.trim()) {
      alert('Digite o nome da tarefa')
      return
    }

    const dataAtual = new Date().toISOString().slice(0, 10)
    onSave(nome.toUpperCase(), dataAtual)
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
      <input
        type="text"
        value={tarefaId || ''}
        disabled
        placeholder="ID"
        className="sm:col-span-1 w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        placeholder="Nome da Tarefa"
        className="sm:col-span-8 w-full p-2 border border-gray-300 rounded-md"
      />
      <div className="sm:col-span-3 flex gap-2">
        <button type="submit" className="bg-green-700 text-white px-4 py-2 rounded w-full hover:bg-green-800">
          {tarefaId ? 'Atualizar' : 'Adicionar'}
        </button>
        {onCancel && (
          <button type="button" onClick={onCancel} className="bg-gray-400 text-white px-4 py-2 rounded w-full hover:bg-gray-500">
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}
