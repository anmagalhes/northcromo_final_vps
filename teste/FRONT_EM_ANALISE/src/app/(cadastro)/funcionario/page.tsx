'use client'
import React, { useState } from 'react'
import axios from 'axios'
import FuncionarioForm from '@/components/funcionario/FuncionarioForm'
import FuncionarioTable from '@/components/funcionario/FuncionarioTable'
import ModalNotificacao from '@/components/ModalNotificacao'
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query'
import useFuncionarioWS from '@/hooks/useFuncionarioWS'
import { Funcionario } from '@/types/funcionario'

export default function FuncionarioCadastro() {
  // Estados do formulário...
  const [nome, setNome] = useState('');
  const [funcaoId, setFuncaoId] = useState<number | null>(null);
  const [status, setStatus] = useState<'ATIVO' | 'INATIVO'>('ATIVO')

  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')
  const [erro, setErro] = useState('')
  const [selecionados, setSelecionados] = useState<number[]>([])

  const [idEditar, setIdEditar] = useState<number | null>(null);
  const [modoEdicaoMultipla, setModoEdicaoMultipla] = useState(false);
  const [editaveis, setEditaveis] = useState<Funcionario[]>([])
  const [loading, setLoading] = useState(false);

  const queryClient = useQueryClient()

  // Busca funções com useQuery
  const { data: funcoes = [], isLoading: funcoesLoading } = useQuery({
    queryKey: ['funcoes'],
    queryFn: () => axios.get('http://localhost:8000/api/funcoes').then(res => res.data),
    staleTime: 1000 * 60 * 5,
  })

  // Hook customizado para funcionários + WebSocket
  const { funcionariosQuery } = useFuncionarioWS()
  const funcionariosRaw: Funcionario[] = funcionariosQuery.data ?? [];

  const funcionariosLoading = funcionariosQuery.isLoading

  // Mapeia os funcionários para exibir na tabela, substituindo funcao pelo nome da função
  const funcionarios = funcionariosRaw.map(f => ({
    id: f.id,
    nome: f.nome,
    funcao_id: f.funcao_id,
    funcao_nome: f.funcao_rel?.funcao_nome || '—',
    status: f.status || 'ATIVO',
    data_cadastro: f.data_cadastro || '',
  }));

  // Função para exclusão em massa
  const excluirFuncionariosEmMassa = async (ids: number[]) => {
    try {
      await Promise.all(ids.map(id => axios.delete(`http://localhost:8000/api/funcionario/${id}`)))
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Funcionários excluídos com sucesso!')
      setModalVisivel(true)
      setSelecionados([]) // Limpar seleção
      queryClient.invalidateQueries({ queryKey: ['funcionarios'] })
    } catch {
      setErro('Erro ao excluir funcionários.')
    }
  }

  // Salvar edição de um funcionário
  const handleSalvarEdicao = async (funcEditado: Funcionario) => {
    setLoading(true)
    try {
      await axios.put(`http://localhost:8000/api/funcionario/${funcEditado.id}`, funcEditado)

      // Atualiza o cache local para refletir a edição
      queryClient.setQueryData<Funcionario[] | undefined>(['funcionarios'], (oldData) => {
        if (!oldData) return []
        return oldData.map(f => (f.id === funcEditado.id ? { ...f, ...funcEditado } : f))
      })

      setIdEditar(null)
      setEditaveis([])
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Funcionário editado com sucesso!')
      setModalVisivel(true)
    } catch (error) {
      console.error('Erro ao salvar edição:', error)
      setErro('Erro ao salvar edição')
    } finally {
      setLoading(false)
    }
  }

  // Cancelar edição
  const handleCancelarEdicao = () => {
    setIdEditar(null)
    setEditaveis([])
  }

  // Iniciar edição de um funcionário
  const handleEdit = (funcionario: Funcionario) => {
    if (funcionario.id != null) {
      setIdEditar(funcionario.id)
      setEditaveis([funcionario])
      setModoEdicaoMultipla(false) // garante que só está editando um
      setSelecionados([]) // limpa seleção ao editar um só
    } else {
      setIdEditar(null)
      setEditaveis([])
    }
  }

  // Edição em massa
  const handleEditarEmMassa = async (funcionariosEditados: Funcionario[]) => {
  setLoading(true);
  setErro('');

  try {
    await Promise.all(funcionariosEditados.map(func =>
      axios.put(`http://localhost:8000/api/funcionario/${func.id}`, func)
    ));

    queryClient.setQueryData<Funcionario[] | undefined>(['funcionarios'], (oldData) => {
      if (!oldData) return []
      return oldData.map(f => {
        const atualizado = funcionariosEditados.find(edit => edit.id === f.id)
        return atualizado ? { ...f, ...atualizado } : f
      })
    })

    setSelecionados([]);
    setModoEdicaoMultipla(false);
    setEditaveis([]);
    setTituloNotificacao('Sucesso');
    setMensagemNotificacao(`Editados ${funcionariosEditados.length} funcionário(s) com sucesso!`);
    setModalVisivel(true);
  } catch (error) {
    console.error('Erro ao editar funcionários:', error);
    setErro('Erro ao editar funcionários em massa');
  } finally {
    setLoading(false);
  }
};

  // Excluir um funcionário
  const handleDelete = async (id: number) => {
    try {
      const response = await axios.delete(`http://localhost:8000/api/funcionario/${id}`)
      if (response.status === 200) {
        queryClient.setQueryData(['funcionarios'], (oldData: Funcionario[] | undefined) => {
          if (!oldData) return []
          return oldData.filter(f => f.id !== id)
        })

        setTituloNotificacao('Sucesso')
        setMensagemNotificacao('Funcionário excluído com sucesso!')
        setModalVisivel(true)
      } else {
        setErro('Erro ao excluir funcionário')
      }
    } catch (error) {
      console.error('Erro ao excluir funcionário:', error)
      setErro('Erro ao excluir funcionário')
    }
  }

  // Mutação para cadastro de funcionário
  const mutation = useMutation({
    mutationFn: (funcionario: Omit<Funcionario, 'id'>) =>
      axios.post('http://localhost:8000/api/funcionario', funcionario),
    onSuccess: () => {
      setTituloNotificacao('Sucesso')
      setMensagemNotificacao('Funcionário cadastrado com sucesso!')
      setModalVisivel(true)
      queryClient.invalidateQueries({ queryKey: ['funcionarios'] })
      limparCampos()
    },
    onError: () => {
      setErro('Erro ao salvar funcionário')
    },
  })

const isSalvando = mutation.status === 'pending'

  // Limpa os campos do formulário
  function limparCampos() {
    setNome('')
    setFuncaoId(null)
    // Removi setSetorId(null) pois setorId não está definido no estado
    setStatus('ATIVO')
    setErro('')
  }

  // Envia dados para cadastro
  const handleEnviar = (
    nome: string,
    funcaoId: number,
    status: 'ATIVO' | 'INATIVO',
    dataCadastro: string
  ) => {
    mutation.mutate({
      nome,
      funcao_id: funcaoId,
      status,
      data_cadastro: dataCadastro,
    });
  };

  // Alterna seleção de um funcionário (checkbox)
  const toggleSelecionado = (id: number) => {
    setSelecionados(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    )
  }

  // Seleciona ou desmarca todos os funcionários
  const toggleSelecionarTodos = () => {
    if (selecionados.length === funcionarios.length) {
      setSelecionados([])
    } else {
      setSelecionados(funcionarios.map(f => f.id))
    }
  }

  // Verifica se todos estão selecionados
  const todosSelecionados = selecionados.length === funcionarios.length && funcionarios.length > 0

  return (
    <div className="min-h-screen bg-slate-100 p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6 text-center">Cadastro de Funcionário</h1>
      <div className="bg-white rounded-lg shadow-md p-6">

        <FuncionarioForm
          nome={nome}
          setNome={setNome}
          funcaoId={funcaoId}
          setFuncaoId={setFuncaoId}
          status={status}
          setStatus={setStatus}
          funcoes={funcoes}
          loading={isSalvando || funcoesLoading}
          onSave={handleEnviar}
          erro={erro}
        />

        <FuncionarioTable
          funcionarios={funcionarios}
          funcoes={funcoes}
          loading={loading || funcionariosLoading}
          selecionados={selecionados}
          toggleSelecionado={toggleSelecionado}
          toggleSelecionarTodos={toggleSelecionarTodos}
          todosSelecionados={todosSelecionados}
          idEditar={idEditar}
          modoEdicaoMultipla={modoEdicaoMultipla}
          setModoEdicaoMultipla={setModoEdicaoMultipla}
          editaveis={editaveis}
          setEditaveis={setEditaveis}
          onEdit={handleEdit}
          onDelete={handleDelete}
          onSalvarEdicao={handleSalvarEdicao}
          onCancelarEdicao={handleCancelarEdicao}
          onDeleteEmMassa={excluirFuncionariosEmMassa}
          onEditarEmMassa={handleEditarEmMassa}
        />

        <ModalNotificacao
          visivel={modalVisivel}
          onFechar={() => setModalVisivel(false)}
          titulo={tituloNotificacao}
          mensagem={mensagemNotificacao}
        />
      </div>
    </div>
  )
}
