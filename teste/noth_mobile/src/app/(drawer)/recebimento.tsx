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
    alert("Você precisa adicionar pelo menos uma foto.");
    return;
  }

  const formData = new FormData();
  formData.append('cliente', cliente);
  formData.append('numero_ordem', numeroControle);

  fotos.forEach((file, index) => {
    formData.append('fotos', file);
  });

  try {
    const response = await axios.post('http://localhost:8000/adicionarOrdem', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        Accept: 'application/json',
      },
    });

    if (response.status === 200) {
      const fileLinks = response.data.file_links;
      if (fileLinks && fileLinks.length > 0) {
        console.log('Links das fotos:', fileLinks);
        const linksFotos = fileLinks.join(', ');
        await salvarLinksFotosNaOrdem(numeroControle, linksFotos);
        alert('Fotos enviadas com sucesso!');
      } else {
        alert('Nenhum link foi gerado para as fotos.');
      }
    } else {
      alert('Erro ao enviar as fotos');
    }
  } catch (error) {
    console.error("Erro ao enviar fotos:", error);
    alert('Erro ao enviar as fotos');
  }
};

    // Função para salvar os links das fotos e os dados adicionais na ordem
    const salvarLinksFotosNaOrdem = async (numeroOrdem, linksFotos) => {
      try {
        // Garantir que só 4 links sejam enviados
        const linksLimitados = linksFotos.slice(0, 4);  // Se houver mais de 4, pegamos apenas os 4 primeiros.

        // Preenche as colunas com os links, colocando null onde não houver link.
        const dadosAdicionais = {
          cliente,
          numero_ordem: numeroOrdem,
          quantidade,
          referencia,
          nfRemessa,
          observacao,
          dataRecebimento,
          horaRecebimento,
          foto1: linksLimitados[0] || null,
          foto2: linksLimitados[1] || null,
          foto3: linksLimitados[2] || null,
          foto4: linksLimitados[3] || null,
        };

        // Enviar os dados para a API que salva os dados na tabela 'ordem_recebimento'
        const response = await axios.post('http://localhost:8000/salvarLinksFotos', dadosAdicionais);

        if (response.status === 200) {
          console.log('Links das fotos e dados adicionais salvos com sucesso!');
          Alert.alert('Sucesso', 'Links das fotos e dados adicionais salvos com sucesso!');
        } else {
          console.log('Erro ao salvar os links das fotos e dados adicionais');
          Alert.alert('Erro', 'Erro ao salvar os links das fotos e dados adicionais');
        }
      } catch (error) {
        console.error('Erro ao salvar os links das fotos e dados adicionais:', error);
        Alert.alert('Erro', 'Erro ao salvar os links das fotos e dados adicionais');
      }
    };

  return (
    <Box
      sx={{
        backgroundColor: '#CBD5E1', // bg-slate-200
        minHeight: '100vh',
        p: 2,
      }}
    >
      {/* Header fake */}
      <Box
        sx={{
          backgroundColor: '#047857', // green-700
          px: 2,
          py: 1,
          mb: 2,
          color: 'white',
          fontWeight: 'bold',
        }}
      >
        {/* Aqui seu Header component */}
        <Typography variant="h6">Header</Typography>
      </Box>

      <Typography variant="h5" fontWeight="bold" color="success.main" mb={3}>
        Cadastro de Nova Ordem
      </Typography>

      {/* Tipo de Ordem */}
      <Stack direction="row" spacing={2} justifyContent="center" mb={4}>
        {['Novo', 'Outro'].map((tipo) => (
          <Button
            key={tipo}
            variant={tipoOrdem === tipo ? 'contained' : 'outlined'}
            color="success"
            onClick={() => setTipoOrdem(tipo)}
          >
            {tipo}
          </Button>
        ))}
      </Stack>

      <Grid container spacing={2}>
        {/* Número de Controle */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Número de Controle"
            variant="outlined"
            value={numeroControle}
            onChange={(e) => setNumeroControle(e.target.value)}
          />
        </Grid>

        {/* Data Recebimento */}
        <Grid item xs={6} sm={3} md={2}>
          <TextField
            fullWidth
            label="Data Recebimento"
            placeholder="DD/MM/AAAA"
            variant="outlined"
            value={dataRecebimento}
            onChange={(e) => setDataRecebimento(e.target.value)}
          />
        </Grid>

        {/* Hora Recebimento */}
        <Grid item xs={6} sm={3} md={2}>
          <TextField
            fullWidth
            label="Hora Recebimento"
            placeholder="HH:MM"
            variant="outlined"
            value={horaRecebimento}
            onChange={(e) => setHoraRecebimento(e.target.value)}
          />
        </Grid>

        {/* Cliente com dropdown */}
        <Grid item xs={12} sm={6} md={4}>
          <Button
            variant="outlined"
            fullWidth
            onClick={abrirDropdownCliente}
            endIcon={
              anchorEl ? (
                <Feather name="chevron-up" size={20} />
              ) : (
                <Feather name="chevron-down" size={20} />
              )
            }
          >
            {cliente || 'Selecione um cliente'}
          </Button>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={fecharDropdownCliente}
          >
            {clientesMock.map((nome) => (
              <MenuItem
                key={nome}
                selected={cliente === nome}
                onClick={() => selecionarCliente(nome)}
              >
                {nome}
              </MenuItem>
            ))}
          </Menu>
        </Grid>

        {/* Quantidade */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Quantidade"
            variant="outlined"
            type="number"
            inputProps={{ min: 1 }}
            value={quantidade}
            onChange={(e) =>
              setQuantidade(e.target.value === '0' ? '1' : e.target.value)
            }
          />
        </Grid>

        {/* ProdutoInput */}
        <Grid item xs={12} md={8}>
          <ProdutoInput
            produtos={produtos}
            codigoProduto={codigoProduto}
            setCodigoProduto={setCodigoProduto}
            nomeProduto={nomeProduto}
            setNomeProduto={setNomeProduto}
            abrirModal={() => setProdutoModalVisivel(true)}
          />
        </Grid>

        {/* ProdutoModal */}
        <ProdutoModal
          visible={produtoModalVisivel}
          onClose={() => setProdutoModalVisivel(false)}
          produtosDisponiveis={produtos}
          onSelect={handleProdutoSelecionado}
        />

        {/* Referência do Produto */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="Referência do Produto"
            variant="outlined"
            value={referencia}
            onChange={(e) => setReferencia(e.target.value)}
          />
        </Grid>

        {/* NF Remessa */}
        <Grid item xs={12} sm={6} md={4}>
          <TextField
            fullWidth
            label="NF Remessa"
            variant="outlined"
            value={nfRemessa}
            onChange={(e) => setNfRemessa(e.target.value)}
          />
        </Grid>

        {/* Observação */}
        <Grid item xs={12}>
          <TextField
            fullWidth
            label="Observação"
            multiline
            minRows={4}
            variant="outlined"
            value={observacao}
            onChange={(e) => setObservacao(e.target.value)}
          />
        </Grid>

        {/* FotoPicker */}
        <Grid item xs={12}>
          <FotoPicker
            nomeCliente={cliente}
            numeroOrdem={numeroControle}
            onAddFoto={handleAddFoto}
          />
        </Grid>

        {/* Botões de ação */}
        <Grid item xs={12}>
          <Stack direction="row" spacing={2} justifyContent="space-between" mt={3}>
            <BotaoAcao
              label="Adicionar"
              cor="verde"
              onPress={enviarFotos}
            />
            <BotaoAcao
              label="Editar"
              cor="azul"
              icone={<Feather name="edit" size={20} color="white" />}
              onPress={() =>
                handleNotificacao('Editar', 'Você está editando esta ordem.')
              }
            />
            <BotaoAcao
              label="Deletar"
              cor="vermelho"
              icone={<Feather name="trash-2" size={20} color="white" />}
              onPress={() =>
                handleNotificacao('Excluir', 'Você está prestes a excluir uma ordem.')
              }
            />
          </Stack>
        </Grid>

        {/* ModalNotificacao */}
        <ModalNotificacao
          visible={modalVisivel}
          onClose={() => setModalVisivel(false)}
          titulo={tituloNotificacao}
          mensagem={mensagemNotificacao}
        />
      </Grid>
    </Box>
  );
}
