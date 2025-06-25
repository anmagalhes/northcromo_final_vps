'use client';

import React, { useState, useEffect } from 'react';
import PostoTrabalhoForm from '@/components/posto_trabalho/Posto_TrabalhoForm';
import PostoTrabalhoTable from '@/components/posto_trabalho/Posto_TrabalhoTable';

interface PostoTrabalhoItem {
  id: number;
  posto_trabalho_nome: string;
  data_execucao: string;
}

export default function PostoTrabalhoPage() {
  const baseURL = 'http://localhost:8000/api';

  const [listaPostos, setListaPostos] = useState<PostoTrabalhoItem[]>([]);

  // Estados de edição
  const [idEditar, setIdEditar] = useState<number | null>(null);
  const [nomeEditar, setNomeEditar] = useState('');
  const [selecionados, setSelecionados] = useState<number[]>([]);
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false);
  const [editaveis, setEditaveis] = useState<PostoTrabalhoItem[]>([]);
  const [loading, setLoading] = useState(false);


    // Verifica se todos estão selecionados
const todosSelecionados = selecionados.length === listaPostos.length && listaPostos.length > 0;

// Função para salvar múltiplos (reaproveitando seu atualizarEmLote)
  const onSalvarMultiplos = async () => {
    await atualizarEmLote();
  };

  // Função para cancelar edição múltipla
  const onCancelarMultiplos = () => {
    setModoEdicaoMultipla(false);
    setSelecionados([]);
    setEditaveis([]);
  };


  // Função para salvar edição individual (item editado)
const onSalvarEdicao = async (item: PostoTrabalhoItem) => {
  try {
    const res = await fetch(`${baseURL}/posto_trabalho/${item.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item),
    });

    if (!res.ok) {
      throw new Error('Erro ao salvar edição');
    }

    // Atualiza a lista localmente após salvar
    setListaPostos(prev =>
      prev.map(p => (p.id === item.id ? item : p))
    );
  } catch {
    alert('Erro ao salvar o item editado.');
  }
};


  // Carrega lista de postos
  useEffect(() => {
    async function fetchPostos() {
      setLoading(true);
      try {
        const res = await fetch(`${baseURL}/posto_trabalho`);
        const data = await res.json();

        if (Array.isArray(data)) {
          setListaPostos(data);
        } else {
          console.error('Resposta da API não é um array:', data);
          setListaPostos([]);
        }
      } catch {
        alert('Erro ao carregar postos de trabalho');
      } finally {
        setLoading(false);
      }
    }
    fetchPostos();
  }, []);

  // Sincroniza itens editáveis para edição múltipla
  useEffect(() => {
    if (modoEdicaoMultipla) {
      const selecionadosEditaveis = listaPostos.filter(p =>
        selecionados.includes(p.id)
      );
      setEditaveis(selecionadosEditaveis);
    } else {
      setEditaveis([]);
    }
  }, [modoEdicaoMultipla, selecionados, listaPostos]);

  // Atualizar o nome no item editável no modo edição múltipla
  const atualizarNomeEditavel = (id: number, novoNome: string) => {
    setEditaveis(prev =>
      prev.map(item =>
        item.id === id ? { ...item, posto_trabalho_nome: novoNome } : item
      )
    );
  };

  // Salvar novo ou editar existente (individual)
  const salvarPosto = async (nome: string) => {
    const corpo = {
      posto_trabalho_nome: nome,
      data_execucao: new Date().toISOString(),
    };

    try {
      const metodo = idEditar ? 'PUT' : 'POST';
      const url = idEditar
        ? `${baseURL}/posto_trabalho/${idEditar}`
        : `${baseURL}/posto_trabalho`;

      const res = await fetch(url, {
        method: metodo,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(corpo),
      });

      const data = await res.json();

      if (res.ok) {
        alert(idEditar ? 'Posto atualizado!' : 'Posto adicionado!');
        setIdEditar(null);
        setNomeEditar('');

        // Recarregar lista após salvar
        const res2 = await fetch(`${baseURL}/posto_trabalho`);
        const updatedList = await res2.json();
        if (Array.isArray(updatedList)) {
          setListaPostos(updatedList);
        } else {
          console.error('Erro ao atualizar a lista, a resposta não é um array:', updatedList);
          setListaPostos([]);
        }
      } else {
        alert(data.detail || 'Erro ao salvar.');
      }
    } catch {
      alert('Erro de conexão.');
    }
  };

  // Excluir um posto
  const deletarPosto = async (id: number) => {
    if (!confirm('Deseja realmente excluir este posto de trabalho?')) return;

    try {
      await fetch(`${baseURL}/posto_trabalho/${id}`, { method: 'DELETE' });
      alert('Posto excluído.');
      setSelecionados(prev => prev.filter(x => x !== id));
      setListaPostos(prev => prev.filter(p => p.id !== id));
    } catch {
      alert('Erro ao excluir.');
    }
  };

  // Excluir selecionados
  const deletarSelecionados = async () => {
    if (selecionados.length === 0) {
      alert('Nenhum posto selecionado.');
      return;
    }

    if (!confirm(`Deseja excluir ${selecionados.length} posto(s)?`)) return;

    try {
      for (const id of selecionados) {
        await fetch(`${baseURL}/posto_trabalho/${id}`, { method: 'DELETE' });
      }
      alert('Postos selecionados excluídos com sucesso.');
      setSelecionados([]);
      setListaPostos(prev => prev.filter(p => !selecionados.includes(p.id)));
    } catch {
      alert('Erro ao excluir postos.');
    }
  };

  // Começar edição de um posto (individual)
  const editarPosto = (item: PostoTrabalhoItem) => {
    setIdEditar(item.id);
    setNomeEditar(item.posto_trabalho_nome);
  };

  // Cancelar edição (individual)
  const cancelarEdicao = () => {
    setIdEditar(null);
    setNomeEditar('');
  };

  // Alternar seleção
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  // Selecionar todos ou limpar seleção
  const toggleSelecionarTodos = () => {
    if (selecionados.length === listaPostos.length) {
      setSelecionados([]);
    } else {
      setSelecionados(listaPostos.map(item => item.id));
    }
  };

  // Atualizar múltiplos em lote
  const atualizarEmLote = async () => {
    try {
      for (const item of editaveis) {
        await fetch(`${baseURL}/posto_trabalho/${item.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(item),
        });
      }
      alert('Postos atualizados com sucesso.');
      setModoEdicaoMultipla(false);
      setSelecionados([]);
      setEditaveis([]);

      // Recarregar lista
      const res2 = await fetch(`${baseURL}/posto_trabalho`);
      const updatedList = await res2.json();
      if (Array.isArray(updatedList)) {
        setListaPostos(updatedList);
      } else {
        console.error('Erro ao atualizar a lista, a resposta não é um array:', updatedList);
        setListaPostos([]);
      }
    } catch {
      alert('Erro ao atualizar postos.');
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 px-4 sm:px-6 md:px-12 py-8">
      <div className="max-w-5xl mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro de Postos de Trabalho
        </h1>

        {/* Formulário individual */}
        {!modoEdicaoMultipla && (
          <PostoTrabalhoForm
            postoId={idEditar ? String(idEditar) : undefined}
            postoNome={nomeEditar}
            onSave={salvarPosto}
            onCancel={idEditar ? cancelarEdicao : undefined}
          />
        )}

        {/* Botões para edição múltipla e exclusão */}
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

        {/* Modo edição múltipla */}
        {modoEdicaoMultipla && (
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-3">Editar Selecionados</h2>

            {editaveis.map(item => (
              <div key={item.id} className="mb-2 flex items-center gap-3">
                <span className="w-8">{item.id}:</span>
                <input
                  type="text"
                  className="border border-gray-300 rounded px-2 py-1 flex-1"
                  value={item.posto_trabalho_nome}
                  onChange={e => atualizarNomeEditavel(item.id, e.target.value)}
                />
              </div>
            ))}

            <div className="flex gap-3 mt-4">
              <button
                onClick={atualizarEmLote}
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
              >
                Salvar Edição em Lote
              </button>
              <button
                onClick={() => setModoEdicaoMultipla(false)}
                className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500 transition"
              >
                Cancelar
              </button>
            </div>
          </div>
        )}

        <PostoTrabalhoTable
        postos={listaPostos}
        onEdit={editarPosto}
        onDelete={deletarPosto}
        selecionados={selecionados}
        toggleSelecionado={toggleSelecionado}
        toggleSelecionarTodos={toggleSelecionarTodos}
        todosSelecionados={todosSelecionados}
        idEditar={idEditar}
        modoEdicaoMultipla={modoEdicaoMultipla}
        editaveis={editaveis}
        setEditaveis={setEditaveis}
        onSalvarMultiplos={onSalvarMultiplos}
        onCancelarMultiplos={onCancelarMultiplos}
        onSalvarEdicao={onSalvarEdicao}
        loading={loading}
        />
      </div>
    </div>
  );
}
