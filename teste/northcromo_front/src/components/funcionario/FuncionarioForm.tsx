'use client';
// src/app/components/componente/FuncaoForm.tsx

import React, { useState } from 'react';

interface Funcao {
  id: number;
  funcao_nome: string;
}

interface FuncionarioFormProps {
  funcionarioId?: number;
  nome: string;
  setNome: (nome: string) => void;
  funcaoId?: number;
  setFuncaoId: (id: number) => void;
  status: 'ATIVO' | 'INATIVO';
  setStatus: (status: 'ATIVO' | 'INATIVO') => void;
  funcoes: Funcao[];
  onSave: (
    nome: string,
  funcaoId: number,
  status: 'ATIVO' | 'INATIVO',
  dataCadastro: string
) => void;
  onCancel?: () => void;
}

export default function FuncionarioForm({
  funcionarioId,
  nome,
  setNome,
  funcaoId,
  setFuncaoId,
  status,
  setStatus,
  funcoes,
  onSave,
  onCancel,
}: FuncionarioFormProps) {
  const [erro, setErro] = useState<string | null>(null);

  const [dataCadastro] = useState(() => {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const spOffset = -3 * 60 * 60000;
    const spDate = new Date(utc + spOffset);
    return spDate.toISOString();
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!nome.trim()) {
      setErro('Nome do funcionário é obrigatório');
      return;
    }
    if (!funcaoId) {
      setErro('Função é obrigatória');
      return;
    }
    setErro(null);
    onSave(nome.trim(), funcaoId, status, dataCadastro);
  };

  return (
    <form onSubmit={handleSubmit} className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6">
      <input
        type="text"
        value={funcionarioId ?? ''}
        disabled
        placeholder="ID do Funcionário"
        className="sm:col-span-2 p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />

      <div className="sm:col-span-5">
        <input
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome do Funcionário"
          className="w-full p-2 border border-green-300 rounded-md"
        />
      </div>

      <div className="sm:col-span-3">
        <select
          value={funcaoId ?? ''}
          onChange={(e) => setFuncaoId(Number(e.target.value))}
          className="w-full p-2 border border-green-300 rounded-md"
        >
          <option value="" disabled>Selecione a Função</option>
          {funcoes.map(f => (
            <option key={f.id} value={f.id}>{f.funcao_nome}</option>
          ))}
        </select>
      </div>

      <div className="sm:col-span-2">
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value === 'ATIVO' ? 'ATIVO' : 'INATIVO')}
          className="w-full p-2 border border-green-300 rounded-md"
        >
          <option value="ATIVO">ATIVO</option>
          <option value="INATIVO">INATIVO</option>
        </select>
      </div>

      {erro && (
        <p className="sm:col-span-12 text-red-600 font-semibold">{erro}</p>
      )}

      <div className="sm:col-span-12 flex gap-2 mt-4">
        <button
          type="submit"
          className="flex-1 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800"
        >
          {funcionarioId ? 'Atualizar' : 'Adicionar'}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
