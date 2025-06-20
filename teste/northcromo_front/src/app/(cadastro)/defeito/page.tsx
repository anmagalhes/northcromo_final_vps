// src/app/defeito/page.tsx
'use client'
import React, { useState, useEffect } from 'react'
import ModalNotificacao from '@/components/ModalNotificacao'
import axios from 'axios'
import DefeitoTable from '@/components/defeito/DefeitoTable'
import useComponentesWS from '@/hooks/useComponentesWS'
import useDefeitoWS from '@/hooks/useDefeitoWS'

export interface Defeito {
  id?: number
  def_nome: string
  data: string
  componente_id: number
  componente_nome?: string
}

export default function DefeitoCadastro() {
  const [defNome, setDefNome] = useState('')
  const [dataDefeito, setDataDefeito] = useState('')
  const [componenteId, setComponenteId] = useState<number | ''>('')
  const [defeitos, setDefeitos] = useState<Defeito[]>([])
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [editaveis, setEditaveis] = useState<Defeito[]>([])
  const todosSelecionados = selecionados.length === defeitos.length && defeitos.length > 0
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)

  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')

  const { componentesQuery } = useComponentesWS()
  const { defeitosQuery } = useDefeitoWS()

  const componentes = componentesQuery.data ?? []
  const componentesLoading = componentesQuery.isLoading
  const componentesError =
    componentesQuery.error instanceof Error ? componentesQuery.error.message : null

// Pega a hora atual de São Paulo
const nowSP = new Date(
  new Date().toLocaleString('pt-BR', {
    timeZone: 'America/Sao_Paulo'
  })
)

  useEffect(() => {
    setDataDefeito(new Date().toISOString().substring(0, 10))
    if (defeitosQuery.data) {
      setDefeitos(defeitosQuery.data)
    }
  }, [defeitosQuery.data])


  function getSaoPauloISOString(dataInput: string): string {
  const [ano, mes, dia] = dataInput.split('-').map(Number);

  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone: 'America/Sao_Paulo',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  });

  const now = new Date();
  const timeParts: any = Object.fromEntries(
    formatter.formatToParts(now).map(({ type, value }) => [type, value])
  );

  const dataSP = `${ano}-${String(mes).padStart(2, '0')}-${String(dia).padStart(2, '0')}T${timeParts.hour}:${timeParts.minute}:${timeParts.second}`;

  return dataSP; // UTC com hora de SP aplicada
}

  const handleEnviar = async () => {
  if (!defNome || !dataDefeito || !componenteId) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  setLoading(true);
  setErro('');

  const dataFinal = getSaoPauloISOString(dataDefeito); // usa hora atual de SP

  const compSelecionado = componentes.find(c => c.id === Number(componenteId));
  const componenteNome = compSelecionado ? compSelecionado.componente_nome : '';

  const dados: Defeito = {
    def_nome: defNome,
    data: dataFinal,
    componente_id: Number(componenteId),
    componente_nome: componenteNome,
  };

  try {
    const response = await axios.post('http://localhost:8000/api/defeito', dados);
    if (response.status === 200 || response.status === 201) {
      setTituloNotificacao('Sucesso');
      setMensagemNotificacao('Defeito cadastrado com sucesso!');
      setModalVisivel(true);
      setDefeitos(prev => [...prev, response.data]);
      setDefNome('');
      setDataDefeito(new Date().toISOString().substring(0, 10));
      setComponenteId('');
    } else {
      setErro('Erro ao salvar defeito');
    }
  } catch (error) {
    console.error('Erro ao salvar defeito:', error);
    setErro('Erro ao salvar defeito');
  } finally {
    setLoading(false);
  }
};

  const handleEdit = (defeito: Defeito) => {
    if (defeito.id != null) {
      setIdEditar(defeito.id)
      setEditaveis([defeito])
      setModoEdicaoMultipla(false)  // Garante que edição simples está ativa
      setSelecionados([])            // Limpa seleção em edição simples
    } else {
      setIdEditar(null)
      setEditaveis([])
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const response = await axios.delete(`http://localhost:8000/api/defeito/${id}`)
      if (response.status === 200) {
        setDefeitos(prev => prev.filter(d => d.id !== id))
        setTituloNotificacao('Sucesso')
        setMensagemNotificacao('Defeito excluído com sucesso!')
        setModalVisivel(true)
      } else {
        setErro('Erro ao excluir defeito')
      }
    } catch (error) {
      console.error('Erro ao excluir defeito:', error)
      setErro('Erro ao excluir defeito')
    }
  }

    const transformarParaPayload = (defeito: Defeito) => ({
    def_nome: defeito.def_nome,
    data: defeito.data,
    componente_id: defeito.componente_id,
  })


  const handleSalvarEdicao = async (itemEditado: Defeito) => {
  setLoading(true)
  try {
    await axios.put(
      `http://localhost:8000/api/defeito/${itemEditado.id}`,
      transformarParaPayload(itemEditado)
    )

    const novosDefeitos = defeitos.map(defeito =>
      defeito.id === itemEditado.id ? itemEditado : defeito
    )
    setDefeitos(novosDefeitos)
    setIdEditar(null)
    setEditaveis([])
    setTituloNotificacao('Sucesso')
    setMensagemNotificacao('Defeito editado com sucesso!')
    setModalVisivel(true)
  } catch (error) {
    console.error('Erro ao salvar edição:', error)
    setErro('Erro ao salvar edição')
  } finally {
    setLoading(false)
  }
}

  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
  }

  const handleDeletarEmMassa = async (ids: number[]) => {
    setLoading(true)
    setErro('')

    try {
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/defeito/${id}`)))

      setDefeitos(prev => prev.filter(d => !ids.includes(d.id!)))
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao(`Excluídos ${ids.length} defeito(s) com sucesso!`)
      setModalVisivel(true)
    } catch (error) {
      console.error('Erro ao excluir defeitos:', error)
      setErro('Erro ao excluir defeitos em massa')
    } finally {
      setLoading(false)
    }
  }

  const handleEditarEmMassa = async (itensEditados: Defeito[]) => {
    setLoading(true)
    setErro('')

    try {
      // Supondo que sua API aceite atualizações em massa, ou faça individualmente:
      await Promise.all(itensEditados.map(item =>
       // axios.put(`http://localhost:8000/api/defeito/${item.id}`, item)
       axios.put(`http://localhost:8000/api/defeito/${item.id}`, transformarParaPayload(item))
      ))

      const novosDefeitos = defeitos.map(defeito => {
        const editado = itensEditados.find(i => i.id === defeito.id)
        return editado ? editado : defeito
      })

      setDefeitos(novosDefeitos)
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao(`Editados ${itensEditados.length} defeito(s) com sucesso!`)
      setModalVisivel(true)
    } catch (error) {
      console.error('Erro ao editar defeitos:', error)
      setErro('Erro ao editar defeitos em massa')
    } finally {
      setLoading(false)
    }
  }

  // Ativa modo edição múltipla e popula editaveis com itens selecionados
  const iniciarEdicaoMultipla = () => {
    const itensParaEditar = defeitos.filter(d => selecionados.includes(d.id!))
    setEditaveis(itensParaEditar)
    setModoEdicaoMultipla(true)
    setIdEditar(null)
  }

  // Cancela a edição múltipla
  const cancelarEdicaoMultipla = () => {
    setModoEdicaoMultipla(false)
    setEditaveis([])
    setSelecionados([])
  }

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Defeito</h1>

      <div className="bg-white p-6 rounded shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:space-x-4">
          <div className="flex-1">
            <label className="block font-medium mb-1">Nome do Defeito</label>
            <input
              type="text"
              value={defNome}
              onChange={e => setDefNome(e.target.value.toUpperCase())}
              className="w-full border p-2 rounded"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Data do Defeito</label>
            <input
              type="date"
              value={dataDefeito}
              onChange={e => setDataDefeito(e.target.value)}
              className="w-full border p-2 rounded"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Componente</label>
            {componentesLoading && <p>Carregando componentes...</p>}
            {componentesError && <p className="text-red-500">{componentesError}</p>}

            {!componentesLoading && !componentesError && (
              <select
                value={componenteId}
                onChange={e => setComponenteId(Number(e.target.value))}
                className="w-full border p-2 rounded"
                disabled={loading}
              >
                <option value="">Selecione um componente</option>
                {componentes.map(c => (
                  <option key={c.id} value={c.id}>
                    {c.componente_nome}
                  </option>
                ))}
              </select>
            )}
          </div>
        </div>

        {erro && <p className="text-red-600">{erro}</p>}

        <button
          onClick={handleEnviar}
          disabled={loading || componentesLoading}
          className="w-full bg-green-700 text-white py-3 rounded font-semibold hover:bg-green-800 disabled:opacity-50"
        >
          {loading ? 'Enviando...' : 'Salvar Defeito'}
        </button>
      </div>


      {modoEdicaoMultipla && (
        <div className="flex justify-end gap-3 mt-4 max-w-5xl mx-auto">
          <button
            onClick={() => {
              const itensSelecionados = editaveis.filter(item => selecionados.includes(item.id!))
              handleEditarEmMassa(itensSelecionados)
            }}
            className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
          >
            Salvar Edição Múltipla
          </button>
          <button
            onClick={cancelarEdicaoMultipla}
            className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
          >
            Cancelar
          </button>
        </div>
      )}

      {/* Tabela de Defeitos */}
      <div className="mt-6">
        <DefeitoTable
          defeitos={defeitos}
          selecionados={selecionados}
          toggleSelecionado={(id) =>
            setSelecionados(prev =>
              prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]
            )
          }
          toggleSelecionarTodos={() => {
            if (selecionados.length === defeitos.length) {
              setSelecionados([])
              setTodosSelecionados(false)
            } else {
              const todosIds = defeitos.map(d => d.id!).filter(Boolean)
              setSelecionados(todosIds)
              setTodosSelecionados(true)
            }
          }}
          todosSelecionados={todosSelecionados}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onSalvarEdicao={handleSalvarEdicao}
          onCancelarEdicao={handleCancelarEdicao}
          componentes={componentes}
          onDeleteEmMassa={handleDeletarEmMassa}
          onEditarEmMassa={handleEditarEmMassa}
        />
      </div>

      <ModalNotificacao
        visivel={modalVisivel}
        onFechar={() => setModalVisivel(false)}
        titulo={tituloNotificacao}
        mensagem={mensagemNotificacao}
      />
    </div>
  )
}
