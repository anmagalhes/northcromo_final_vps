  import React, { useState, useEffect } from 'react';
  import { View, Text, TextInput, ScrollView, Pressable, Alert } from 'react-native';
  import * as ImagePicker from 'expo-image-picker';
  import { Feather } from '@expo/vector-icons';
  import * as Notifications from 'expo-notifications';
  import ModalNotificacao from '../../components/ModalNotificacao'; // Modal de Notificação
  import { Header } from "../../components/header";
  import * as FileSystem from 'expo-file-system';
  import axios from 'axios';


  import { useNavigation } from '@react-navigation/native';
  import Constants from 'expo-constants';
  import { uploadFotosParaAPI } from '../../utils/fileUpload';
  import { enviarOrdemComFotos } from '../../api/ordens';


  const statusBarHeight = Constants.statusBarHeight;

  import ProdutoInput from '../../components/ProdutoInput'; // Componente de Autocomplete para Produto
  import ProdutoModal from '../../components/ProdutoModal'; // Modal para selecionar produto
  import FotoPicker from '../../components/FotoPicker'; // Componente para Adicionar Fotos
  import BotaoAcao from '../../components/BotaoAcao';

  import { getDataHoraSaoPaulo } from '../../utils/DataHora';

  interface Foto {
    id: string;
    uri: string;
  }

  export default function Recebimento() {
    const [fotos, setFotos] = useState<Foto[]>([]); // Estado que vai armazenar as fotos

    // Função que recebe as fotos do filho e atualiza o estado
    const handleAddFoto = (novasFotos: Foto[]) => {
      setFotos(novasFotos);
    };

    const navigation = useNavigation();

    const [tipoOrdem, setTipoOrdem] = useState<'Novo' | 'Outro'>('Novo');
    const [numeroControle, setNumeroControle] = useState('');
    const [dataRecebimento, setDataRecebimento] = useState('');
    const [horaRecebimento, setHoraRecebimento] = useState('');
    const [cliente, setCliente] = useState('');
    const [mostrarListaClientes, setMostrarListaClientes] = useState(false);
    const [quantidade, setQuantidade] = useState('1');
    const [referencia, setReferencia] = useState('');
    const [nfRemessa, setNfRemessa] = useState('');
    const [observacao, setObservacao] = useState('');


    interface FotoInfo {
      uri: string;
      name: string;
      type: string;
    }

    // Campos de Produto
    const [codigoProduto, setCodigoProduto] = useState('');
    const [nomeProduto, setNomeProduto] = useState('');

    // Estado do modal
    const [produtoModalVisivel, setProdutoModalVisivel] = useState(false);

    // Modal de Notificação
    const [modalVisivel, setModalVisivel] = useState(false);
    const [tituloNotificacao, setTituloNotificacao] = useState('');
    const [mensagemNotificacao, setMensagemNotificacao] = useState('');


    // Destacar o campo ativo
    const [campoAtivo, setCampoAtivo] = useState<string>('');

    // Lista de produtos cadastrados
    const produtosCadastrados = [
      { codigo: '123', nome: 'Parafuso 3mm' },
      { codigo: '456', nome: 'Chapa Aço Inox' },
      { codigo: '789', nome: 'Eixo Central' },
    ];

    // Função para buscar produtos do backend
    const carregarProdutos = async () => {
      setLoading(true); // Inicia o loading enquanto busca os produtos
          try {
            // Simulação de dados de produtos
        const produtosMock = [
          { codigo: '123', nome: 'Parafuso 3mm' },
          { codigo: '456', nome: 'Chapa Aço Inox' },
          { codigo: '789', nome: 'Eixo Central' },
        ];

        // Faça a requisição para o seu backend para carregar os produtos
        //const response = await axios.get('https://api.seuservidor.com/produtos'); // Substitua com sua URL real
        //setProdutos(response.data); // Atualiza o estado de produtos com os dados retornados do backend
       setProdutos(produtosMock); // Atualiza o estado de produtos com dados mockados
      } catch (error) {
        setErro('Erro ao carregar os produtos'); // Em caso de erro, exibe uma mensagem
      } finally {
        setLoading(false); // Finaliza o loading, independentemente de sucesso ou erro
      }
    };

    const [produtos, setProdutos] = useState([]); // ← ESSENCIAL para não dar erro
    const [loading, setLoading] = useState(false);
    const [erro, setErro] = useState('');

    // Chama a função de carregar produtos assim que o componente for montado
    useEffect(() => {
      carregarProdutos(); // Chama a função para carregar os produtos
    }, []); // O array vazio faz o efeito rodar apenas uma vez, quando o componente for montado

    // Mock de clientes
    const clientesMock = ['Tony Stark', 'Bruce Wayne', 'Diana Prince'];


    // Setar data e hora automaticamente
    useEffect(() => {
      const { data, hora } = getDataHoraSaoPaulo();
      setDataRecebimento(data);
      setHoraRecebimento(hora);
    }, []);


    // Função que lida com a seleção do produto no modal
    const handleProdutoSelecionado = (indice: number) => {
      const produtoSelecionado = produtos[indice]; // ou algo similar, dependendo do formato da resposta da API
      if (!produtoSelecionado) {
        console.warn('Produto não encontrado no índice:', indice);
        return;
      }
      setCodigoProduto(produtoSelecionado.codigo);
      setNomeProduto(produtoSelecionado.nome);
      setProdutoModalVisivel(false);
    };

    // Função que simula a busca da última ordem
    const buscarUltimaOrdem = async (): Promise<string> => {
      const ultimaOrdem = '0256';
      const proxima = String(Number(ultimaOrdem) + 1).padStart(4, '0');
      return proxima;
    };

    // Dispara sempre que o tipo de ordem for alterado
    useEffect(() => {
      const atualizarNumeroOrdem = async () => {
        if (tipoOrdem === 'Novo') {
          const novoNumero = await buscarUltimaOrdem();
          setNumeroControle(novoNumero);
        } else {
          setNumeroControle('');
        }
      };

      atualizarNumeroOrdem();
    }, [tipoOrdem]);

    // Função de envio de notificação
    const handleNotificacao = (titulo: string, mensagem: string) => {
      setTituloNotificacao(titulo);
      setMensagemNotificacao(mensagem);
      setModalVisivel(true); // Exibe o modal
    };

    const getMimeTypeFromUri = (uri: string): string => {
      const extension = uri.split('.').pop();
      switch (extension) {
        case 'jpg':
        case 'jpeg':
          return 'image/jpeg';
        case 'png':
          return 'image/png';
        default:
          return 'image/jpeg'; // Caso o tipo não seja conhecido, assume o tipo 'jpeg'
      }
    };

    // 🔁 Primeiro: essa função precisa estar antes de `enviarFotos`
    const base64ToBlob = (base64: string, mimeType: string) => {
      const byteCharacters = atob(base64);
      const byteArrays = [];

      for (let offset = 0; offset < byteCharacters.length; offset += 512) {
        const slice = byteCharacters.slice(offset, offset + 512);
        const byteNumbers = new Array(slice.length);

        for (let i = 0; i < slice.length; i++) {
          byteNumbers[i] = slice.charCodeAt(i);
        }

        const byteArray = new Uint8Array(byteNumbers);
        byteArrays.push(byteArray);
      }

      return new Blob(byteArrays, { type: mimeType });
    };


    const enviarFotos = async () => {
      if (fotos.length === 0) {
        Alert.alert("Nenhuma foto", "Você precisa adicionar pelo menos uma foto.");
        return;
      }

      // Cria um FormData para enviar as fotos
      const formData = new FormData();

      // Adiciona o nome do cliente ao FormData
      formData.append('cliente', cliente);

      // Adicionando as fotos ao FormData
      fotos.forEach((foto, index) => {
        console.log(`Foto ${index + 1}:`);
        console.log("URI:", foto.uri);
        console.log("Tipo:", foto.type);
        console.log("Nome:", foto.name);

        const mimeType = foto.type || 'image/jpeg';
        const fileName = foto.name || `foto_${index + 1}.jpg`;

        // Cria o Blob a partir do base64
        const blob = base64ToBlob(foto.base64, mimeType);

        // Transforma em um "file" (com nome e tipo)
        const file = new File([blob], fileName, { type: mimeType });

        // Adiciona ao FormData
        formData.append('fotos', file);
      });

      // (opcional) log para ver se o formData está ok
      for (const pair of formData.entries()) {
        console.log(`${pair[0]}:`, pair[1]);
      }

      try {
        // Realizando a requisição POST com Axios
        const response = await axios.post('http://localhost:8000/adicionarOrdem', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
            Accept: 'application/json',
          },
        });

        if (response.status === 200) {
          // Obtemos os links das fotos retornados pela API
          const fileLinks = response.data.file_links;

          if (fileLinks && fileLinks.length > 0) {
            // Exibe os links das fotos carregadas
            fileLinks.forEach((link, index) => {
              console.log(`Link da Foto ${index + 1}: ${link}`);
            });

            // Exibe o alerta de sucesso com os links
            Alert.alert('Sucesso', 'Fotos enviadas com sucesso!\n' + fileLinks.join('\n'));
          } else {
            Alert.alert('Erro', 'Nenhum link foi gerado para as fotos.');
          }
        } else {
          Alert.alert('Erro', 'Erro ao enviar as fotos');
        }
      } catch (error) {
        console.error("Erro ao enviar fotos:", error);
        Alert.alert('Erro', 'Erro ao enviar as fotos');
      }
    };

    return (

      <ScrollView style={{ flex: 1 }} className="bg-slate-200" showsVerticalScrollIndicator={false}>
      <View className="w-full px-4 bg-green-700" style={{ marginTop: statusBarHeight + 8 }}>
        <Header openDrawer={() => navigation.openDrawer()} />
      </View>

      <View className="px-2 py-2">
              <Text className="text-lg font-bold text-green-700">Cadastro de Nova Ordem</Text>
            </View>

        {/* Tipo de Ordem */}
        <View className="flex-row justify-center mb-4 gap-4">
          {['Novo', 'Outro'].map(tipo => (
            <Pressable
              key={tipo}
              onPress={() => setTipoOrdem(tipo as 'Novo' | 'Outro')}
              className={`px-4 py-2 rounded-full ${
                tipoOrdem === tipo ? 'bg-green-700' : 'bg-gray-300'
              }`}
            >
              <Text className="text-white font-bold">{tipo}</Text>
            </Pressable>
          ))}
        </View>

        {/* Número de Controle */}
        <Text className="text-gray-700 mb-1">Número de Controle</Text>
        <TextInput
          className={`border border-gray-300 rounded px-3 py-2 mb-4 ${
            campoAtivo === 'numeroControle' ? 'bg-white' : 'bg-gray-50'
          }`}
          value={numeroControle}
          onChangeText={setNumeroControle}
          onFocus={() => setCampoAtivo('numeroControle')}
          onBlur={() => setCampoAtivo('')}
        />

        {/* Data e Hora */}
        <View className="flex-row gap-4 mb-4">
          <View className="flex-1">
            <Text className="text-gray-700 mb-1">Data Recebimento</Text>
            <TextInput
              placeholder="DD/MM/AAAA"
              className="border border-gray-300 rounded px-3 py-2"
              value={dataRecebimento}
              onChangeText={setDataRecebimento}
              onFocus={() => setCampoAtivo('numeroControle')}
              onBlur={() => setCampoAtivo('')}
            />
          </View>

          <View className="flex-1">
            <Text className="text-gray-700 mb-1">Hora Recebimento</Text>
            <TextInput
              placeholder="HH:MM"
              className="border border-gray-300 rounded px-3 py-2"
              value={horaRecebimento}
              onChangeText={setHoraRecebimento}
              onFocus={() => setCampoAtivo('numeroControle')}
              onBlur={() => setCampoAtivo('')}
            />
          </View>
        </View>

        {/* Cliente com dropdown */}
        <Text className="text-gray-700 mb-1">Cliente</Text>
        <Pressable
          onPress={() => setMostrarListaClientes(!mostrarListaClientes)}
          className="flex-row justify-between items-center border border-gray-300 rounded px-3 py-2 bg-white shadow-sm mb-1"
        >
          <Text className={`text-base ${cliente ? 'text-black' : 'text-gray-400'}`}>
            {cliente || 'Selecione um cliente'}
          </Text>
          <Feather name={mostrarListaClientes ? 'chevron-up' : 'chevron-down'} size={20} color="#555" />
        </Pressable>

        {mostrarListaClientes && (
          <View className="border border-gray-300 rounded mb-4 bg-white shadow-md">
            {clientesMock.map(nome => (
              <Pressable
                key={nome}
                className={`px-4 py-3 border-b border-gray-200 ${
                  cliente === nome ? 'bg-green-100' : 'bg-white'
                }`}
                onPress={() => {
                  setCliente(nome);
                  setMostrarListaClientes(false);
                }}
              >
                <Text className="text-sm text-gray-800">{nome}</Text>
              </Pressable>
            ))}
          </View>
        )}

        {/* Quantidade */}
        <Text className="text-gray-700 mb-1">Quantidade</Text>
        <TextInput
          keyboardType="numeric"
          className={`border border-gray-300 rounded px-3 py-2 mb-4 ${
            campoAtivo === 'quantidade' ? 'bg-white' : 'bg-gray-50'
          }`}
          value={quantidade}
          onChangeText={text => setQuantidade(text === '0' ? '1' : text)}
          onFocus={() => setCampoAtivo('quantidade')}
          onBlur={() => setCampoAtivo('')}
        />

        {/* Produto com autocomplete e ícone de lupa */}
        <ProdutoInput
         // produtos={carregarProdutos}
          produtos={produtos} // ← ✅ Correto agora
          codigoProduto={codigoProduto}
          setCodigoProduto={setCodigoProduto}
          nomeProduto={nomeProduto}
          setNomeProduto={setNomeProduto}
          abrirModal={() => setProdutoModalVisivel(true)} // Abre o modal ao clicar no campo
        />

        {/* Modal de Produto */}
        <ProdutoModal
          visible={produtoModalVisivel}
          onClose={() => setProdutoModalVisivel(false)}
         // produtosDisponiveis={carregarProdutos}
          produtosDisponiveis={produtos}
          onSelect={handleProdutoSelecionado} // Passa a função para manipular a seleção do produto
        />

        {/* Referência do Produto */}
        <Text className="text-gray-700 mb-1">Referência do Produto</Text>
        <TextInput
          className={`border border-gray-300 rounded px-3 py-2 mb-4 ${
            campoAtivo === 'referencia' ? 'bg-white' : 'bg-gray-50'
          }`}
          value={referencia}
          onChangeText={setReferencia}
          onFocus={() => setCampoAtivo('referencia')}  // Quando o campo ganha foco
          onBlur={() => setCampoAtivo('')}             // Quando o campo perde o foco
        />

        {/* NF Remessa */}
        <Text className="text-gray-700 mb-1">NF Remessa</Text>
        <TextInput
          className={`border border-gray-300 rounded px-3 py-2 mb-4 ${
            campoAtivo === 'nfRemessa' ? 'bg-white' : 'bg-gray-50'
          }`}
          value={nfRemessa}
          onChangeText={setNfRemessa}
          onFocus={() => setCampoAtivo('nfRemessa')}  // Quando o campo ganha foco
          onBlur={() => setCampoAtivo('')}            // Quando o campo perde o foco
        />

        {/* Observação */}
        <Text className="text-gray-700 mb-1">Observação</Text>
        <TextInput
          multiline
          className={`border border-gray-300 rounded px-3 py-2 mb-4 h-20 ${
            campoAtivo === 'observacao' ? 'bg-white' : 'bg-gray-50'
          }`}
          value={observacao}
          onChangeText={setObservacao}
          onFocus={() => setCampoAtivo('observacao')}  // Quando o campo ganha foco
          onBlur={() => setCampoAtivo('')}            // Quando o campo perde o foco
        />


        {/* Fotos */}

          {/* Componente FotoPicker recebe o nome do cliente e a função onAddFoto */}
          <FotoPicker
          nomeCliente={cliente}
          numeroOrdem={numeroControle}
          onAddFoto={handleAddFoto}
        />

        <View className="flex-row justify-between mt-6 mb-10 gap-3">
          <BotaoAcao
          label="Adicionar"
          cor="verde"
          onPress={() => {
            console.log('Botão pressionadosssss');
            enviarFotos();
          }}
          />''
          <BotaoAcao
            label="Editar"
            cor="azul"
            icone={<Feather name="edit" size={20} color="white" />}  // Ícone 'edit'
            onPress={() => handleNotificacao('Editar', 'Você está editando esta ordem.')}
          />
          <BotaoAcao
            label="Deletar"
            cor="vermelho"
            icone={<Feather name="trash-2" size={20} color="white" />}  // Ícone 'trash-2'
            onPress={() => handleNotificacao('Excluir', 'Você está prestes a excluir uma ordem.')}
          />
        </View>

        {/* Modal de Notificação */}
        <ModalNotificacao
          visible={modalVisivel}
          onClose={() => setModalVisivel(false)}
          titulo={tituloNotificacao}
          mensagem={mensagemNotificacao}
        />
      </ScrollView>
    );
  }
