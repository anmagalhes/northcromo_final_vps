// src/components/operacao/OperacaoForm.tsx
import React, { useState, useEffect } from 'react'

interface Props {
  operacaoId?: string
  operacaoNome?: string
  operacaoGrupo?: string;
  onSave: (nome: string, grupo: string) => void;
  onCancel?: () => void
}

export default function OperacaoForm({
  operacaoId,
  operacaoNome = '',
  operacaoGrupo = '',
  onSave,
  onCancel,
}: Props) {
  const [nome, setNome] = useState(operacaoNome)
  const [grupo, setGrupo] = useState(operacaoGrupo);

  useEffect(() => {
    setNome(operacaoNome);
    setGrupo(operacaoGrupo);
  }, [operacaoNome, operacaoGrupo]);

   useEffect(() => {
    // Sempre mantém no máximo 3 caracteres (em maiúsculo)
    setGrupo(nome.slice(0, 3).toUpperCase());
  }, [nome]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!nome.trim()) {
      alert('Digite o nome da operação')
      return
    }
    onSave(nome.toUpperCase(), grupo.toUpperCase());
  }

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
       {/* Campo ID (opcional) */}
      <input
        type="text"
        value={operacaoId || ''}
        disabled
        placeholder="ID"
        className="sm:col-span-1 w-full p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />
       {/* Campo Nome da Operação */}
      <input
        type="text"
        value={nome}
        onChange={(e) => setNome(e.target.value.toUpperCase())}
        placeholder="Nome da Operação"
        className="sm:col-span-5 w-full p-2 border border-gray-300 rounded-md"
      />
      {/* Campo Grupo do Processo */}
      <input
        type="text"
        value={grupo}
        onChange={(e) => setGrupo(e.target.value)}
        placeholder="Grupo do Processo"
        className="sm:col-span-3 w-full p-2 border border-gray-300 rounded-md"
      />

       {/* Botões */}
      <div className="sm:col-span-3 flex gap-2">
        <button
          type="submit"
          className="flex items-center justify-center gap-2 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 transition w-full"
        >
          {operacaoId ? 'Atualizar' : 'Adicionar'}
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
