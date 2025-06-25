'use client'
import React, { useState, useEffect } from 'react'
import axios from 'axios'
import ModalNotificacao from '@/components/ModalNotificacao'
import ProdutoTable from '@/components/produto/ProdutoTable'
import useComponentesWS from '@/hooks/useComponentesWS'
import useProdutoWS from '@/hooks/useProdutosWS'

export interface Produto {
  id?: number
  cod_produto: string
  produto_nome: string
  data: string
  componente_id: number
  operacao_id: number
  posto_trabalho_id: number
  componente_nome?: string
  operacao_nome?: string
  posto_trabalho_nome?: string
  und_servicos?: string
  grupo_id?: string
  tipo_produto?: number
}

export default function ProdutoCadastro() {
  const [codProduto, setCodProduto] = useState('')
  const [produtoNome, setProdutoNome] = useState('')
  const [dataProduto, setDataProduto] = useState('')
  const [componenteId, setComponenteId] = useState<number | ''>('')
  const [operacaoId, setOperacaoId] = useState<number | ''>('')
  const [postoTrabalhoId, setPostoTrabalhoId] = useState<number | ''>('')
  const [produtos, setProdutos] = useState<Produto[]>([])
  const [selecionados, setSelecionados] = useState<number[]>([])
  const [idEditar, setIdEditar] = useState<number | null>(null)
  const [editaveis, setEditaveis] = useState<Produto[]>([])
  const todosSelecionados = selecionados.length === produtos.length && produtos.length > 0
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false)

  //const [componentes, setComponentes] = useState<OptionItem[]>([])
  //const [operacoes, setOperacoes] = useState<OptionItem[]>([]);
  //const [postosTrabalho, setPostosTrabalho] = useState<OptionItem[]>([]);

  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')

  const { componentesQuery } = useComponentesWS()
  const { produtosQuery } = useProdutoWS()

  const componentes = componentesQuery.data ?? []
  const componentesLoading = componentesQuery.isLoading
  const componentesError =
    componentesQuery.error instanceof Error ? componentesQuery.error.message : null

  const [undServicos, setUndServicos] = useState('');
  const [grupoId, setGrupoId] = useState('');
  const [tipoProduto, setTipoProduto] = useState<number | ''>('');

  const [itemParaSalvar, setItemParaSalvar] = React.useState<Produto | null>(null);

  const operacoes = [
    { id: 1, nome: 'Operação 1' },
    { id: 2, nome: 'Operação 2' },
    { id: 3, nome: 'Operação 3' }
  ]
  const postosTrabalho = [
    { id: 1, nome: 'Posto 1' },
    { id: 2, nome: 'Posto 2' },
    { id: 3, nome: 'Posto 3' }
  ]

  useEffect(() => {
    setDataProduto(new Date().toISOString().substring(0, 10))
    if (produtosQuery.data) {
      setProdutos(produtosQuery.data)
    }
  }, [produtosQuery.data])

  function getSaoPauloISOString(dataInput: string): string {
    const [ano, mes, dia] = dataInput.split('-').map(Number)

    const formatter = new Intl.DateTimeFormat('en-US', {
      timeZone: 'America/Sao_Paulo',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: false,
    })

    const now = new Date()
    const timeParts: any = Object.fromEntries(
      formatter.formatToParts(now).map(({ type, value }) => [type, value])
    )

    const dataSP = `${ano}-${String(mes).padStart(2, '0')}-${String(dia).padStart(2, '0')}T${timeParts.hour}:${timeParts.minute}:${timeParts.second}`

    return dataSP
  }

  const handleEnviar = async () => {
  if (!produtoNome || !dataProduto || !componenteId || !operacaoId || !postoTrabalhoId) {
    alert('Preencha todos os campos obrigatórios');
    return;
  }

  setLoading(true);
  setErro('');

  const dataFinal = getSaoPauloISOString(dataProduto); // usa hora atual de SP

  const compSelecionado = componentes.find(c => c.id === Number(componenteId));
  const componenteNome = compSelecionado ? compSelecionado.componente_nome : '';

  const dados: Produto = {
    cod_produto: codProduto,
    produto_nome: produtoNome,
    data: dataFinal,
    componente_id: Number(componenteId),
    operacao_id: Number(operacaoId),
    posto_trabalho_id: Number(postoTrabalhoId),
    und_servicos: undServicos,
    grupo_id: grupoId,
    tipo_produto: tipoProduto,

    //mponente_nome: componenteNome,
    //eracao_nome: operacoes.find(o => o.id === Number(operacaoId))?.nome || '',
    //sto_trabalho_nome: postosTrabalho.find(p => p.id === Number(postoTrabalhoId))?.nome || ''
  };

  try {
    const response = await axios.post('http://localhost:8000/api/produto', dados);
    if (response.status === 200 || response.status === 201) {
      setTituloNotificacao('Sucesso');
      setMensagemNotificacao('Produto cadastrado com sucesso!');
      setModalVisivel(true);
      setProdutos(prev => [...prev, response.data]);
      setCodProduto('');
      setProdutoNome('');
      setDataProduto(new Date().toISOString().substring(0, 10));
      setComponenteId('');
      setOperacaoId('');
      setPostoTrabalhoId('');
    } else {
      setErro('Erro ao salvar produto');
    }
  } catch (error) {
    console.error('Erro ao salvar produto:', error);
    setErro('Erro ao salvar produto');
  } finally {
    setLoading(false);
  }
};

  const handleEdit = (produto: Produto) => {
    if (produto.id != null) {
      setIdEditar(produto.id)
      setEditaveis([produto])
      setModoEdicaoMultipla(false) // Garante que edição simples está ativa
      setSelecionados([]) // Limpa seleção em edição simples
    } else {
      setIdEditar(null)
      setEditaveis([])
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const response = await axios.delete(`http://localhost:8000/api/produto/${id}`)
      if (response.status === 200) {
        setProdutos(prev => prev.filter(p => p.id !== id))
        setTituloNotificacao('Sucesso')
        setMensagemNotificacao('Produto excluído com sucesso!')
        setModalVisivel(true)
      } else {
        setErro('Erro ao excluir produto')
      }
    } catch (error) {
      console.error('Erro ao excluir produto:', error)
      setErro('Erro ao excluir produto')
    }
  }

  const handleSalvarEdicao = async (itemEditado: Produto) => {
    setLoading(true)
    try {
      await axios.put(`http://localhost:8000/api/produto/${itemEditado.id}`, itemEditado)

      const novosProdutos = produtos.map(produto =>
        produto.id === itemEditado.id ? itemEditado : produto
      )
      setProdutos(novosProdutos)
      setIdEditar(null)
      setEditaveis([])
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Produto editado com sucesso!')
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
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/produto/${id}`)))

      setProdutos(prev => prev.filter(p => !ids.includes(p.id!)))
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao(`Excluídos ${ids.length} produto(s) com sucesso!`)
      setModalVisivel(true)
    } catch (error) {
      console.error('Erro ao excluir produtos:', error)
      setErro('Erro ao excluir produtos em massa')
    } finally {
      setLoading(false)
    }
  }

  const handleEditarEmMassa = async (itensEditados: Produto[]) => {
    setLoading(true)
    setErro('')

    try {
      await Promise.all(itensEditados.map(item =>
        axios.put(`http://localhost:8000/api/produto/${item.id}`, item)
      ))

      const novosProdutos = produtos.map(produto => {
        const editado = itensEditados.find(i => i.id === produto.id)
        return editado ? editado : produto
      })

      setProdutos(novosProdutos)
      setSelecionados([])
      setModoEdicaoMultipla(false)
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao(`Editados ${itensEditados.length} produto(s) com sucesso!`)
      setModalVisivel(true)
    } catch (error) {
      console.error('Erro ao editar produtos:', error)
      setErro('Erro ao editar produtos em massa')
    } finally {
      setLoading(false)
    }
  }

  // Ativa modo edição múltipla e popula editaveis com itens selecionados
  const iniciarEdicaoMultipla = () => {
    const itensParaEditar = produtos.filter(p => selecionados.includes(p.id!))
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

  useEffect(() => {
  if (!itemParaSalvar) return;

  const timer = setTimeout(async () => {
    setLoading(true);
    setErro('');
    try {
      await axios.put(`http://localhost:8000/api/produto/${itemParaSalvar.id}`, itemParaSalvar);

      setProdutos(prev =>
        prev.map(prod => (prod.id === itemParaSalvar.id ? itemParaSalvar : prod))
      );

      setTituloNotificacao('Sucesso');
      setMensagemNotificacao('Produto editado com sucesso!');
      setModalVisivel(true);
      setIdEditar(null);
      setEditaveis([]);
    } catch (error) {
      console.error('Erro ao salvar edição:', error);
      setErro('Erro ao salvar edição');
    } finally {
      setLoading(false);
      setItemParaSalvar(null);
    }
  }, 1000); // 1 segundo debounce

  return () => clearTimeout(timer);
}, [itemParaSalvar]);

const atualizarEditavel = (campo: keyof Produto, valor: any) => {
  setEditaveis(prev => prev.map(item => {
    if (item.id === idEditar) {
      return { ...item, [campo]: valor }
    }
    return item
  }))
}

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Produto</h1>

      <div className="bg-white p-6 rounded shadow-md space-y-4">
        <div className="flex flex-col sm:flex-row sm:space-x-4">
          <div className="flex-1">
            <label className="block font-medium mb-1">Código do Produto</label>
            <input
              type="text"
              value={codProduto}
              onChange={e => setCodProduto(e.target.value)}
              className="w-full border p-2 rounded"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Nome do Produto</label>
            <input
              type="text"
              value={produtoNome}
              onChange={e => setProdutoNome(e.target.value.toUpperCase())}
              className="w-full border p-2 rounded"
              disabled={loading}
            />
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Data do Produto</label>
            <input
              type="date"
              value={dataProduto}
              onChange={e => setDataProduto(e.target.value)}
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

        <div className="flex flex-col sm:flex-row sm:space-x-4">
          <div className="flex-1">
            <label className="block font-medium mb-1">Operação</label>
            <select
              value={operacaoId}
              onChange={e => setOperacaoId(Number(e.target.value))}
              className="w-full border p-2 rounded"
              disabled={loading}
            >
              <option value="">Selecione uma operação</option>
              {operacoes.map(o => (
                <option key={o.id} value={o.id}>
                  {o.nome}
                </option>
              ))}
            </select>
          </div>

          <div className="flex-1">
            <label className="block font-medium mb-1">Posto de Trabalho</label>
            <select
              value={postoTrabalhoId}
              onChange={e => setPostoTrabalhoId(Number(e.target.value))}
              className="w-full border p-2 rounded"
              disabled={loading}
            >
              <option value="">Selecione um posto de trabalho</option>
              {postosTrabalho.map(p => (
                <option key={p.id} value={p.id}>
                  {p.nome}
                </option>
              ))}
            </select>
          </div>
        </div>

      <div className="flex-1">
        <label className="block font-medium mb-1">Unidade de Serviço</label>
        <input
          type="text"
          value={undServicos}
          onChange={e => setUndServicos(e.target.value.toUpperCase())}
          className="w-full border p-2 rounded"
          disabled={loading}
        />
      </div>

      <div className="flex-1">
        <label className="block font-medium mb-1">Grupo</label>
        <select
          value={grupoId}
          onChange={e => setGrupoId(e.target.value)}
          className="w-full border p-2 rounded"
          disabled={loading}
        >
          <option value="">Selecione o grupo</option>
          <option value="PRODUTO">PRODUTO</option>
          <option value="SERVICO">SERVIÇO</option>
        </select>
      </div>

      <div className="flex-1">
        <label className="block font-medium mb-1">Tipo de Produto</label>
        <select
          value={tipoProduto}
          onChange={e => setTipoProduto(Number(e.target.value))}
          className="w-full border p-2 rounded"
          disabled={loading}
        >
          <option value="">Selecione o tipo</option>
          <option value={1}>Produto</option>
          <option value={2}>Tarefa</option>
        </select>
      </div>

        {erro && <p className="text-red-600">{erro}</p>}

        <button
          onClick={handleEnviar}
          disabled={loading}
          className="w-full bg-green-700 text-white py-3 rounded font-semibold hover:bg-green-800 disabled:opacity-50"
        >
          {loading ? 'Enviando...' : 'Salvar Produto'}
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

      {/* Tabela de Produtos */}
      <div className="mt-6">
        <ProdutoTable
        produtos={produtos || []}
        selecionados={selecionados || []}
        editaveis={editaveis || []}
        componentes={componentes || []}  // ✅ Esta linha estava faltando
        operacoes={operacoes || []}
        postosTrabalho={postosTrabalho || []}
        toggleSelecionado={(id) =>
          setSelecionados(prev =>
            prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]
          )
        }
        toggleSelecionarTodos={() => {
          if (selecionados.length === produtos.length) {
            setSelecionados([])
          } else {
            const todosIds = produtos.map(p => p.id!).filter(Boolean)
            setSelecionados(todosIds)
          }
        }}
        todosSelecionados={todosSelecionados}
        idEditar={idEditar}
        modoEdicaoMultipla={modoEdicaoMultipla}
        setEditaveis={setEditaveis}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onSalvarEdicao={handleSalvarEdicao}
        onCancelarEdicao={handleCancelarEdicao}
        onDeleteEmMassa={handleDeletarEmMassa}
        onEditarEmMassa={handleEditarEmMassa}
        onChangeEditavel={atualizarEditavel}
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
