'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { FiEdit, FiTrash2, FiChevronDown, FiChevronUp } from 'react-icons/fi'
import ModalNotificacao from '@/components/ModalNotificacao'
import ProdutoInput from '@/components/ProdutoInput'
import ProdutoModal from '@/components/ProdutoModal'
import BotaoAcao from '@/components/BotaoAcao'
import axios from 'axios'
import { useRef } from 'react';

import { getDataHoraSaoPaulo } from '../../../utils/DataHora'

import { useClientes } from '@/hooks/useClientes';
import { useProdutos } from '@/hooks/useProdutos';

interface Produto {
  codigo: string
  nome: string
}

export default function Recebimento() {
  const router = useRouter()

  // Query React - lado usuario
  //const { data: produtos = [], isLoading: loadingProdutos } = useProdutos();
  //const { data: clientes = [], isLoading: loadingClientes } = useClientes();

  // Estados do formulário
  const [tipoOrdem, setTipoOrdem] = useState<'NOVO' | 'NAO'>('NOVO')
  const [numeroControle, setNumeroControle] = useState('')

   //Ordem nova
  const [ordemBase, setOrdemBase] = useState<string | null>(null)
  const [numeroOrdem, setNumeroOrdem] = useState('');
  const [numeroOrdemFormatado, setNumeroOrdemFormatado] = useState('');

  const [dataRecebimento, setDataRecebimento] = useState('')
  const [horaRecebimento, setHoraRecebimento] = useState('')
  const [cliente, setCliente] = useState('')
  const [mostrarListaClientes, setMostrarListaClientes] = useState(false)
  const [quantidade, setQuantidade] = useState('1')
  const [referencia, setReferencia] = useState('')
  const [nfRemessa, setNfRemessa] = useState('')
  const [observacao, setObservacao] = useState('')

  // Fotos: armazenar array de arquivos
  const [fotos, setFotos] = useState<File[]>([])
  const inputFileRef = useRef<HTMLInputElement | null>(null);

  // Produto selecionado
  const [codigoProduto, setCodigoProduto] = useState('')
  const [nomeProduto, setNomeProduto] = useState('')
  const [produtoModalVisivel, setProdutoModalVisivel] = useState(false)

  // Modal notificação
  const [modalVisivel, setModalVisivel] = useState(false)
  const [tituloNotificacao, setTituloNotificacao] = useState('')
  const [mensagemNotificacao, setMensagemNotificacao] = useState('')

  // Loading e erro para envio
  const [loading, setLoading] = useState(false)
  const [erro, setErro] = useState('')

  // Produtos e clientes mockados
  const [produtos, setProdutos] = useState<Produto[]>([])
  const clientesMock = ['Tony Stark', 'Bruce Wayne', 'Diana Prince']

  // Campo ativo para estilo
  const [campoAtivo, setCampoAtivo] = useState('')

    useEffect(() => {
    const carregarNumeroOrdem = async () => {
      try {
        const response = await fetch('http://localhost:8000/ordemnova')
        const data = await response.json()

        if (data.proximo_numero_ordem) {
          const ordemFormatada = String(data.proximo_numero_ordem).padStart(4, '0')
          setOrdemBase(ordemFormatada)
          setNumeroOrdem(ordemFormatada)
        }
      } catch (error) {
        console.error('Erro ao carregar número da ordem:', error)
        setErro('Erro ao carregar número da ordem')
      }
    }

    carregarNumeroOrdem()
  }, [])


  // Carregar produtos mockados
  const carregarProdutos = async () => {
    setLoading(true)
    try {
      // Mock de produtos
      const produtosMock = [
        { codigo: '123', nome: 'Parafuso 3mm' },
        { codigo: '456', nome: 'Chapa Aço Inox' },
        { codigo: '789', nome: 'Eixo Central' },
      ]
      setProdutos(produtosMock)
    } catch (error) {
      setErro('Erro ao carregar os produtos')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    carregarProdutos()
  }, [])

  // Setar data e hora na montagem
  useEffect(() => {
    const { data, hora } = getDataHoraSaoPaulo()
    setDataRecebimento(data)
    setHoraRecebimento(hora)
  }, [])

  // Atualizar número de ordem ao mudar tipoOrdem
  useEffect(() => {
    // Só roda se ordemBase tiver valor válido
    if (!ordemBase) return;

    const buscarUltimaOrdem = async (): Promise<string> => {

      // Aqui ordemBase já tem valor, só calcula próximo
      const proxima = String(Number(ordemBase)).padStart(4, '0');
      return proxima;
    };

    const atualizarNumeroOrdem = async () => {

      if (tipoOrdem === 'NOVO') {
        const novoNumero = await buscarUltimaOrdem();
        const anoAtual = new Date().getFullYear().toString().slice(-2);
        const numeroFormatado = `${novoNumero}-${anoAtual}`;

        setNumeroControle(numeroFormatado);  //INPUNT
        setNumeroOrdemFormatado(novoNumero); // BANCO

       // setNumeroControle(novoNumero);
        console.log('Numero Controle atualizado para:', novoNumero);
      } else {
        setNumeroControle('');
        setNumeroOrdemFormatado('');
      }
    };

  atualizarNumeroOrdem();
}, [tipoOrdem, ordemBase]);

  // Selecionar produto do modal
  const handleProdutoSelecionado = (indice: number) => {
    const produtoSelecionado = produtos[indice]
    if (!produtoSelecionado) {
      console.warn('Produto não encontrado no índice:', indice)
      return
    }
    setCodigoProduto(produtoSelecionado.codigo)
    setNomeProduto(produtoSelecionado.nome)
    setProdutoModalVisivel(false)
  }

  // Adicionar fotos selecionadas (input file)
  const handleAddFotos = (files: FileList | null) => {
  if (!files) return
  const arquivos = Array.from(files)

  setFotos(prev => {
    if (prev.length + arquivos.length > 4) {
      alert('Você só pode adicionar até 4 fotos.')
      return prev
    }
    return [...prev, ...arquivos]
  })
}

 // Remover foto por índice
  const removerFoto = (index: number) => {
    setFotos(prev => prev.filter((_, i) => i !== index))
  }


  // Função para enviar fotos e dados
    const enviarFotos = async () => {
      if (fotos.length === 0) {
        alert('Você precisa adicionar pelo menos uma foto.')
        return
      }
      setLoading(true)

      const formData = new FormData()
      formData.append('cliente', cliente)
      formData.append('numero_ordem', numeroControle)

      fotos.forEach((foto) => {
        formData.append('fotos', foto)
      })

      try {
        const response = await axios.post('http://localhost:8000/api/adicionarOrdem', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })

        if (response.status === 200) {
          const fileLinks = response.data.file_links
          console.log('Links das fotos:', fileLinks)

          // Espera salvar os links antes de seguir
          await salvarLinksFotosNaOrdem(numeroControle, fileLinks)
          alert('Fotos enviadas com sucesso!')

          // Resetar input de fotos e estado
          setFotos([])
          if (inputFileRef.current) {
            inputFileRef.current.value = '' // <-- limpa o input visualmente
          }

          setCliente('');
          setQuantidade('1');
          setCodigoProduto('');
          setNomeProduto('');
          setReferencia('');
          setNfRemessa('');
          setObservacao('');

          // **Atualizar número da ordem após envio**
          try {
            const novaOrdemResponse = await fetch('http://localhost:8000/api/ordemnova');
            const novaOrdemData = await novaOrdemResponse.json();

            if (typeof novaOrdemData === 'number') {
              const novaOrdemFormatada = novaOrdemData.toString().padStart(4, '0');
              setOrdemBase(novaOrdemFormatada);
              setNumeroOrdem(novaOrdemFormatada);

              if (tipoOrdem === 'NOVO') {
                const proximaOrdem = String(Number(novaOrdemFormatada) + 1).padStart(4, '0');
                setNumeroControle(proximaOrdem);
              } else {
                setNumeroControle('');
              }
            } else {
              console.error('Formato inesperado na resposta da ordem nova:', novaOrdemData);
            }
          } catch (error) {
            console.error('Erro ao buscar nova ordem após envio:', error);
          }

        // ✅ Resetar a página (refrescar componentes do App Router)
        router.refresh()

        } else {
          alert('Erro ao enviar as fotos');
        }
      } catch (error) {
        console.error('Erro ao enviar fotos:', error);
        alert('Erro ao enviar as fotos');
      } finally {
        setLoading(false);
      }
    };


  const salvarLinksFotosNaOrdem = async (numeroOrdem: string, linksFotos: string[]) => {
    try {
      const linksLimitados = linksFotos.slice(0, 4)

      const dadosAdicionais = {
        cliente,
        tipoOrdem,
        numero_ordem: tipoOrdem === 'NOVO' ? numeroOrdemFormatado :'0',
        os_formatado: numeroOrdem,
        quantidade: Number(quantidade),
        referencia,
        nfRemessa,
        queixa_cliente: observacao,
        dataRecebimento,
        horaRecebimento,
        foto1: linksLimitados[0] || null,
        foto2: linksLimitados[1] || null,
        foto3: linksLimitados[2] || null,
        foto4: linksLimitados[3] || null,
      }

    console.log('Dados que serão enviados:', dadosAdicionais);

      const response = await axios.post('http://localhost:8000/api/salvarLinksFotos', dadosAdicionais)

      if (response.status === 200) {
        console.log('Links das fotos e dados adicionais salvos com sucesso!')
        alert('Links das fotos e dados salvos com sucesso!')
      } else {
        alert('Erro ao salvar os links das fotos e dados')
      }
    } catch (error) {
      console.error('Erro ao salvar os links das fotos e dados adicionais:', error)
      alert('Erro ao salvar os links')
    }
  }

  const handleNotificacao = (titulo: string, mensagem: string) => {
    setTituloNotificacao(titulo)
    setMensagemNotificacao(mensagem)
    setModalVisivel(true)
  }

    useEffect(() => {
      async function fetchNumeroOrdem() {
        try {
          const response = await fetch('http://localhost:8000/api/ordemnova');
          const data = await response.json();

          if (typeof data === 'number') {
            const ordemFormatada = data.toString().padStart(4, '0');
            setOrdemBase(ordemFormatada);
            setNumeroOrdem(ordemFormatada);

            // 👇 Já calcula e define aqui, evitando esperar NAO useEffect
            if (tipoOrdem === 'NOVO') {
              const proxima = String(Number(ordemFormatada) + 1).padStart(4, '0');
              setNumeroControle(proxima);
              console.log('Numero Controle definido diretamente após fetch:', proxima);
            }
          } else {
            console.error('Número de ordem inesperado:', data);
          }
        } catch (error) {
          console.error('Erro ao buscar número de ordem:', error);
        }
      }

  fetchNumeroOrdem();
}, []);

  return (
   <div className="min-h-screen bg-slate-100 px-2 sm:px-4 md:px-6">
       <div className="w-full py-6">
        <h1 className="text-2xl font-bold text-green-700 mb-6 text-center">
          Cadastro de Nova Ordem</h1>

        <div className="bg-white rounded-lg shadow-md p-6">
          {/* Tipo de Ordem */}
          <div className="flex justify-center mb-6 gap-4 flex-wrap">
            {['NOVO', 'NAO'].map(tipo => (
              <button
                key={tipo}
                onClick={() => setTipoOrdem(tipo as 'NOVO' | 'NAO')}
                className={`px-4 py-2 rounded-full transition-colors min-w-[100px] text-center ${
                  tipoOrdem === tipo
                    ? 'bg-green-700 text-white'
                    : 'bg-gray-200 hover:bg-gray-300'
                }`}
              >
                {tipo}
              </button>
            ))}
          </div>

          {/* Formulário */}
          <div className="space-y-4">
            {/* Número de Controle */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Número de Controle
              </label>
              <input
                type="text"
                className={`w-full p-2 border rounded-md ${
                  campoAtivo === 'numeroControle' ? 'ring-2 ring-blue-400 border-blue-400' : 'border-gray-300'
                }`}
                value={numeroControle}
                onChange={e => setNumeroControle(e.target.value)}
                onFocus={() => setCampoAtivo('numeroControle')}
                onBlur={() => setCampoAtivo('')}
                placeholder="Número da ordem"
              />
            </div>

            {/* Data e Hora */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Data Recebimento
                </label>
                <input
                  type="text"
                  className="w-full p-2 border border-gray-300 rounded-md bg-gray-50 cursor-not-allowed"
                  value={dataRecebimento}
                  readOnly
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Hora Recebimento
                </label>
                <input
                  type="text"
                  className="w-full p-2 border border-gray-300 rounded-md bg-gray-50 cursor-not-allowed"
                  value={horaRecebimento}
                  readOnly
                />
              </div>
            </div>

            {/* Cliente */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Cliente
              </label>
              <div className="relative">
                <button
                  onClick={() => setMostrarListaClientes(!mostrarListaClientes)}
                  className="flex justify-between items-center w-full p-2 border border-gray-300 rounded-md bg-white"
                  type="button"
                >
                  <span className={cliente ? 'text-gray-800' : 'text-gray-400'}>
                    {cliente || 'Selecione um cliente'}
                  </span>
                  {mostrarListaClientes ? <FiChevronUp /> : <FiChevronDown />}
                </button>

                {mostrarListaClientes && (
                  <div className="absolute z-10 mt-1 w-full bg-white border border-gray-300 rounded-md shadow-lg max-h-48 overflow-auto">
                    {clientesMock.map(nome => (
                      <button
                        key={nome}
                        className={`block w-full text-left p-2 hover:bg-gray-100 ${
                          cliente === nome ? 'bg-green-50' : ''
                        }`}
                        onClick={() => {
                          setCliente(nome)
                          setMostrarListaClientes(false)
                        }}
                        type="button"
                      >
                        {nome}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Quantidade */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Quantidade
              </label>
              <input
                type="number"
                min="1"
                className="w-full p-2 border border-gray-300 rounded-md"
                value={quantidade}
                onChange={e => setQuantidade(e.target.value)}
              />
            </div>

            {/* Produto */}
            <ProdutoInput
              produtos={produtos}
              codigoProduto={codigoProduto}
              setCodigoProduto={setCodigoProduto}
              nomeProduto={nomeProduto}
              setNomeProduto={setNomeProduto}
              abrirModal={() => setProdutoModalVisivel(true)}
            />

            {/* Produto Modal */}
            <ProdutoModal
              aberto={produtoModalVisivel}
              onClose={() => setProdutoModalVisivel(false)}
              produtos={produtos}
              onSelect={handleProdutoSelecionado}
            />

            {/* Referência */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Referência do Produto
              </label>
              <input
                type="text"
                className="w-full p-2 border border-gray-300 rounded-md"
                value={referencia}
                onChange={e => setReferencia(e.target.value)}
              />
            </div>

            {/* NF Remessa */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                NF Remessa
              </label>
              <input
                type="text"
                className="w-full p-2 border border-gray-300 rounded-md"
                value={nfRemessa}
                onChange={e => setNfRemessa(e.target.value)}
              />
            </div>

            {/* Observação */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Observação
              </label>
              <textarea
                className="w-full p-2 border border-gray-300 rounded-md resize-none"
                rows={3}
                value={observacao}
                onChange={e => setObservacao(e.target.value)}
                placeholder="Observações adicionais..."
              />
            </div>

            {/* Upload de fotos */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Adicionar Fotos (máx 4)
              </label>

              <input
                ref={inputFileRef}
                type="file"
                accept="image/*"
                capture="environment"
                multiple
                onChange={e => handleAddFotos(e.target.files)}
                className="block w-full text-sm text-gray-500
                           file:mr-4 file:py-2 file:px-4
                           file:rounded-full file:border-0
                           file:text-sm file:font-semibold
                           file:bg-green-700 file:text-white
                           hover:file:bg-green-800
                           cursor-pointer"
              />

              {/* Visualizar thumbnails das fotos adicionadas */}
              <div className="mt-3 grid grid-cols-2 sm:grid-cols-4 gap-4">
                {fotos.map((foto, idx) => {
                  const url = URL.createObjectURL(foto)
                  return (
                    <div
                      key={idx}
                      className="relative w-24 h-24 rounded-md overflow-hidden border border-gray-300 shadow-sm"
                    >
                      <img
                        src={url}
                        alt={`Foto ${idx + 1}`}
                        className="object-cover w-full h-full"
                      />
                      <button
                        onClick={() =>
                          setFotos(prev => prev.filter((_, i) => i !== idx))
                        }
                        className="absolute top-1 right-1 bg-red-600 text-white rounded-full p-1 text-xs hover:bg-red-700"
                        title="Remover foto"
                      >
                        ×
                      </button>
                    </div>
                  )
                })}
              </div>
            </div>


            {/* Botões */}
            <div className="flex flex-col sm:flex-row gap-4 mt-6">
              <button
                onClick={enviarFotos}
                disabled={loading}
                className="flex-1 bg-green-700 hover:bg-green-800 text-white font-semibold py-3 rounded-md disabled:opacity-60 transition"
              >
                {loading ? 'Enviando...' : 'Enviar Fotos'}
              </button>

              <BotaoAcao
                label="Editar"
                cor="azul"
                icone={<FiEdit size={18} />}
                onPress={() => handleNotificacao('Editar', 'Você está editando esta ordem.')}
              />

               <BotaoAcao
                label="Deletar"
                cor="vermelho"
                icone={<FiTrash2 size={18} />}
                onPress={() => handleNotificacao('Excluir', 'Você está prestes a excluir uma ordem.')}
              />

              <button
                onClick={() => router.push('/')}
                className="flex-1 border border-gray-300 hover:bg-gray-100 rounded-md py-3 font-semibold"
              >
                Voltar
              </button>
            </div>
          </div>
        </div>

        {/* Modal notificação */}
        <ModalNotificacao
          aberto={modalVisivel}
          onClose={() => setModalVisivel(false)}
          titulo={tituloNotificacao}
          mensagem={mensagemNotificacao}
        />
      </div>
    </div>
  )
}

