//src/app/components/componente/ComponenteForm.tsx
import React, { useState, useEffect } from 'react'

interface Props {
  componenteId?: string
  componenteNome?: string
  onSave: (nome: string) => void
  onCancel?: () => void
}

export default function ComponenteForm({ componenteId, componenteNome = '', onSave, onCancel }: Props) {
  const [nome, setNome] = useState(componenteNome)

  useEffect(() => {
    setNome(componenteNome)
  }, [componenteNome])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nome.trim()) {
      alert('Digite o nome do componente')
      return
    }
    onSave(nome.toUpperCase())
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
      <input
        type="text"
        value={componenteId || ''}
        disabled
        placeholder="ID"
        className="sm:col-span-3 w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value)}
        placeholder="Nome do Componente"
        className="sm:col-span-6 w-full p-2 border border-gray-300 rounded-md"
      />
      <div className="sm:col-span-3 flex gap-2">
        <button
          type="submit"
          className="flex items-center justify-center gap-2 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition w-full"
        >
          {componenteId ? 'Atualizar' : 'Adicionar'}
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
