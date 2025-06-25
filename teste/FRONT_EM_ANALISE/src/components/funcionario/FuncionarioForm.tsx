'use client';
import React, { useState, useEffect } from 'react';

interface Funcao {
  id: number;
  funcao_nome: string;
}

interface FuncionarioFormProps {
  funcionarioId?: number;
  nome: string;
  setNome: (nome: string) => void;
  funcaoId: number | null | undefined;
  setFuncaoId: (id: number | null) => void;
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
  loading: boolean;
  erro: string;
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
  loading,
  erro,
}: FuncionarioFormProps) {
  const [erroLocal, setErroLocal] = useState<string | null>(null);
  const [dataCadastro, setDataCadastro] = useState('');

  // Definir data de cadastro no primeiro render
  useEffect(() => {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const spOffset = -3 * 60 * 60000;
    const spDate = new Date(utc + spOffset);
    setDataCadastro(spDate.toISOString());
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validação simples
    if (!nome.trim()) {
      setErroLocal('Nome do funcionário é obrigatório');
      return;
    }

    if (!funcaoId) {
      setErroLocal('Função é obrigatória');
      return;
    }

    setErroLocal(null);
    onSave(nome.trim(), funcaoId, status, dataCadastro);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="grid grid-cols-1 sm:grid-cols-12 gap-4 mb-6"
    >
      {/* Campo ID - somente leitura */}
      <input
        type="text"
        value={funcionarioId ?? ''}
        disabled
        placeholder="ID"
        className="sm:col-span-2 p-2 border border-gray-300 rounded-md bg-gray-100 text-center"
      />

      {/* Campo Nome */}
      <div className="sm:col-span-5">
        <input
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Nome do Funcionário"
          className="w-full p-2 border border-green-300 rounded-md"
          disabled={loading}
        />
      </div>

      {/* Campo Função */}
      <div className="sm:col-span-3">
        <select
          value={funcaoId ?? ''}
          onChange={(e) => setFuncaoId(Number(e.target.value))}
          className="w-full p-2 border border-green-300 rounded-md"
          disabled={loading || funcoes.length === 0}
        >
          <option value="" disabled>
            {funcoes.length === 0 ? 'Carregando funções...' : 'Selecione a Função'}
          </option>
          {funcoes.map((f) => (
            <option key={f.id} value={f.id}>
              {f.funcao_nome}
            </option>
          ))}
        </select>
      </div>

      {/* Campo Status */}
      <div className="sm:col-span-2">
        <select
          value={status}
          onChange={(e) =>
            setStatus(e.target.value === 'ATIVO' ? 'ATIVO' : 'INATIVO')
          }
          className="w-full p-2 border border-green-300 rounded-md"
          disabled={loading}
        >
          <option value="ATIVO">ATIVO</option>
          <option value="INATIVO">INATIVO</option>
        </select>
      </div>

      {/* Mensagens de erro */}
      {(erroLocal || erro) && (
        <p className="sm:col-span-12 text-red-600 font-semibold">
          {erroLocal || erro}
        </p>
      )}

      {/* Botões */}
      <div className="sm:col-span-12 flex gap-2 mt-4">
        <button
          type="submit"
          disabled={loading}
          className="flex-1 px-4 py-2 bg-green-700 text-white rounded-md hover:bg-green-800 disabled:opacity-50"
        >
          {loading
            ? funcionarioId ? 'Atualizando...' : 'Adicionando...'
            : funcionarioId ? 'Atualizar' : 'Adicionar'}
        </button>

        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={loading}
            className="flex-1 px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 disabled:opacity-50"
          >
            Cancelar
          </button>
        )}
      </div>
    </form>
  );
}
