// src/components/posto_trabalho/PostoTrabalhoForm.tsx
import React, { useState, useEffect } from 'react'

interface Props {
  postoId?: string
  postoNome?: string
  onSave: (nome: string, dataExecucao: string, id?: string) => void
  onCancel?: () => void
}

export default function PostoTrabalhoForm({
  postoId,
  postoNome = '',
  onSave,
  onCancel,
}: Props) {
  const [nome, setNome] = useState(postoNome)

  useEffect(() => {
    setNome(postoNome)
  }, [postoNome])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nome.trim()) {
      alert('Digite o nome do posto de trabalho')
      return
    }

    // Data de execução = data atual do sistema em ISO (YYYY-MM-DD)
    const dataAtual = new Date().toISOString().slice(0, 10)
     onSave(nome.toUpperCase(), dataAtual)
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
      <input
        type="text"
        value={postoId || ''}
        disabled
        placeholder="ID"
        className="sm:col-span-1 w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        placeholder="Nome do Posto de Trabalho"
        className="sm:col-span-8 w-full p-2 border border-gray-300 rounded-md"
      />

      {/* Remove campo data */}

      <div className="sm:col-span-3 flex gap-2">
        <button
          type="submit"
          className="flex items-center justify-center gap-2 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition w-full"
        >
          {postoId ? 'Atualizar' : 'Adicionar'}
        </button>
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-gray-400 text-white rounded-md hover:bg-gray-500 transition w-full"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  )
}
