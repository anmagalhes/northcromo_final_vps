//src/app/operacao/page.tsx
'use client';

import React, { useState, useEffect,  useMemo  } from 'react';
import useOperacoesWS from '@/hooks/useOperacoesWS';
import OperacaoForm from '@/components/operacao/OperacaoForm';
import OperacaoTable from '@/components/operacao/OperacaoTable';

import { OperacaoItem } from '@/types/operacao';

export default function OperacaoPage() {
  const { operacoesQuery } = useOperacoesWS();
  const listaOperacoes = useMemo(() => operacoesQuery.data || [], [operacoesQuery.data]);
  //const listaOperacoes = operacoesQuery.data || [];
//  const loading = operacoesQuery.isLoading;

  const [idEditar, setIdEditar] = useState<number | null>(null);
  const [nomeEditar, setNomeEditar] = useState('');
  const [grupoEditar, setGrupoEditar] = useState('');
  const [selecionados, setSelecionados] = useState<number[]>([]);
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false);
  const [editaveis, setEditaveis] = useState<OperacaoItem[]>([]);

  const baseURL = 'http://localhost:8000/api';

  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listaOperacoes.filter(o =>
        selecionados.includes(o.id)
      );
      setEditaveis(selecionadosEditaveis);
    }
  }, [modoEdicaoMultipla, selecionados, listaOperacoes]);

  const salvarOperacao = async (nome: string, grupo: string) => {
    const corpo = {
      op_nome: nome,
      op_grupo_processo: grupo,
      data_execucao: new Date().toISOString(),
    };

    try {
      const metodo = idEditar ? 'PUT' : 'POST';
      const url = idEditar
        ? `${baseURL}/operacao/${idEditar}`
        : `${baseURL}/operacao`;

      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      });

      const data = await res.json();

      if (res.ok) {
        alert(idEditar ? 'Operação atualizada!' : 'Operação adicionada!');
        setIdEditar(null);
        setNomeEditar('');
        setGrupoEditar('');
      } else {
        alert(data.detail || 'Erro ao salvar.');
      }
    } catch {
      alert('Erro de conexão.');
    }
  };

  const deletarOperacao = async (id: number) => {
    if (!confirm('Deseja realmente excluir esta operação?')) return;

    try {
      await fetch(`${baseURL}/operacao/${id}`, { method: 'DELETE' });
      alert('Operação excluída.');
      setSelecionados(prev => prev.filter(x => x !== id));
    } catch {
      alert('Erro ao excluir.');
    }
  };

  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhuma operação selecionada.');
      return;
    }

    if (!confirm(`Deseja excluir ${selecionados.length} operação(ões)?`)) return;

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/operacao/${id}`, { method: 'DELETE' });
      }
      alert('Operações selecionadas excluídas com sucesso.');
      setSelecionados([]);
    } catch {
      alert('Erro ao excluir operações.');
    }
  };

  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/operacao/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        });
      }
      alert('Operações atualizadas com sucesso.');
      setModoEdicaoMultipla(false);
      setSelecionados([]);
      setEditaveis([]);
    } catch {
      alert('Erro ao atualizar operações.');
    }
  };

  const editarOperacao = (item: OperacaoItem) => {
    setIdEditar(item.id);
    setNomeEditar(item.op_nome);
    setGrupoEditar(item.op_grupo_processo);
  };

  const cancelarEdicao = () => {
    setIdEditar(null);
    setNomeEditar('');
    setGrupoEditar('');
  };

  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  const toggleSelecionarTodos = () => {
    if (selecionados.length === listaOperacoes.length) {
      setSelecionados([]);
    } else {
      setSelecionados(listaOperacoes.map(item => item.id));
    }
  };

  const salvarEdicaoIndividual = async (item: OperacaoItem) => {
  try {
    const res = await fetch(`${baseURL}/operacao/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item),
    });

    const data = await res.json();

    if (!res.ok) {
      alert(data.detail || 'Erro ao atualizar operação individual.');
    }
  } catch {
    alert('Erro de conexão ao editar operação individual.');
  }
};


  return (
    <div className="min-h-screen bg-slate-100 px-4 sm:px-6 md:px-12 py-8">
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro de Operações
        </h1>

        <OperacaoForm
          operacaoId={idEditar ? String(idEditar) : undefined}
          operacaoNome={nomeEditar}
          operacaoGrupo={grupoEditar}
          onSave={salvarOperacao}
          onCancel={idEditar ? cancelarEdicao : undefined}
        />

        {selecionados.length > 0 && !modoEdicaoMultipla && (
          <div className="mb-4 flex justify-end gap-3">
            <button
              onClick={() => setModoEdicaoMultipla(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Editar Selecionadas ({selecionados.length})
            </button>
            <button
              onClick={deletarSelecionados}
              className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition"
            >
              Excluir Selecionadas ({selecionados.length})
            </button>
          </div>
        )}

        <OperacaoTable
          operacoes={listaOperacoes}
          onEdit={editarOperacao}
          onDelete={deletarOperacao}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={selecionados.length === listaOperacoes.length && listaOperacoes.length > 0}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onSalvarMultiplos={atualizarEmLote}
          onCancelarMultiplos={() => {
            setModoEdicaoMultipla(false);
            setEditaveis([]);
          }}
          onSalvarEdicao={salvarEdicaoIndividual}
        />
      </div>
    </div>
  );
}
