import React, { useState } from 'react';
import { View, Image, Pressable, Text, Modal, TouchableOpacity, Alert } from 'react-native';
import { Feather } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';

interface Foto {
  id: string;  // ID único da foto
  uri: string; // URI da foto
  base64: string; // 🆕 imagem codificada
}

interface Props {
  nomeCliente: string; // Passa o nome do cliente como prop
  numeroOrdem: string; // 👈 novo prop
  onAddFoto: (foto: Foto) => void; // Passa um objeto foto com ID e URI
}

const gerarNomeFoto = (ordemIndex: number) => {
  const hoje = new Date();
  const dia = String(hoje.getDate()).padStart(2, '0');
  const mes = String(hoje.getMonth() + 1).padStart(2, '0');
  const ano = String(hoje.getFullYear()).slice(-2); // último 2 dígitos

  const nomeFormatado = nomeCliente.replace(/\s/g, ''); // remove espaços
  return `foto_Ordem${numeroOrdem}_${nomeFormatado}_${dia}-${mes}-${ano}_${indice + 1}.jpg`;
};


export default function FotoPicker({ nomeCliente,  numeroOrdem, onAddFoto }: Props) {
  const [fotos, setFotos] = useState<Foto[]>([]);  // Estado que armazena objetos com ID e URI
  const [fotoTemp, setFotoTemp] = useState<string | null>(null); // Foto temporária para visualização
  const [cameraType, setCameraType] = useState<ImagePicker.CameraType>(ImagePicker.CameraType.back); // Tipo de câmera
  const [modalVisible, setModalVisible] = useState(false); // Estado para controlar o modal

  // Função para gerar ID da foto com base no número e nome do cliente
  const gerarIdFoto = (ordem: number) => {
    return `${nomeCliente}_foto_${ordem}`;
  };


    // Função para pegar o tipo MIME com base na extensão da URI
const getMimeTypeFromUri = (uri: string): string => {
  const extension = uri.split('.').pop(); // Extrai a extensão do arquivo
  switch (extension) {
    case 'jpg':
    case 'jpeg':
      return 'image/jpeg';
    case 'png':
      return 'image/png';
    default:
      return 'image/jpeg'; // Caso o tipo não seja conhecido, assume 'jpeg' como padrão
  }
};

// Função para escolher uma foto da galeria
const handleFotoEscolher = async () => {
  // Solicitar permissão para a galeria
  const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();

  // Se a permissão não for concedida, exibe um alerta
  if (permissionResult.granted === false) {
    Alert.alert("Permissão negada", "Precisamos da permissão para acessar sua galeria");
    return;
  }

  // Lança o seletor de imagens
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images, // Apenas imagens
    quality: 0.6,  // Qualidade da imagem
    base64: true,  // Codifica a imagem em base64 (se necessário)
  });

  // Verifica se a foto foi escolhida e se o limite de fotos não foi alcançado
  if (!result.canceled && fotos.length < 4) {
    const asset = result.assets[0]; // Pega a primeira imagem selecionada

    // Gera um ID único para a foto
    const idFoto = gerarIdFoto(fotos.length + 1);

    // Determina o tipo MIME da imagem. Se for base64, usamos o tipo inferido pelo nome da extensão do arquivo.
    const mimeType = asset.base64
      ? getMimeTypeFromUri(asset.uri) // Se for base64, tentamos pegar o MIME pela extensão da URI
      : asset.type || 'image/jpeg'; // Se a imagem tem o tipo, usamos ele. Se não, usamos 'image/jpeg'

    // Gera um nome único para a foto
    const nomeFoto = `foto_${idFoto}_${Date.now()}.jpg`;

    // Cria o objeto da nova foto
    const novaFoto = {
      id: idFoto,               // ID único da foto
      uri: asset.uri,           // URI da foto (base64 ou caminho)
      base64: asset.base64 || '',  // Base64 da foto (se disponível)
      type: mimeType,           // Tipo da foto (determinado pela URI ou tipo do asset)
      name: nomeFoto,           // Nome da foto
    };

    // Atualiza o estado local com a nova foto
    const novasFotos = [...fotos, novaFoto];
    setFotos(novasFotos);  // Atualiza o estado local de fotos

    // Passa a lista de fotos atualizada para o pai
    onAddFoto(novasFotos);
  } else {
    // Se o limite de fotos for alcançado, exibe um alerta
    Alert.alert("Limite de fotos", "Você atingiu o limite de 4 fotos.");
  }
};

  // Função para tirar uma foto com a câmera
  const handleFotoTirar = async () => {
    const permissionResult = await ImagePicker.requestCameraPermissionsAsync();
    if (permissionResult.granted === false) {
      Alert.alert("Permissão negada", "Precisamos da permissão para acessar sua câmera");
      return;
    }

    const result = await ImagePicker.launchCameraAsync({
      quality: 0.6,
      base64: true,
      type: cameraType,
    });

    if (!result.canceled && fotos.length < 4) {
      const asset = result.assets[0];
      const idFoto = gerarIdFoto(fotos.length + 1); // Gera um ID único para a foto


      // Usa a função para obter o tipo MIME baseado na URI da imagem
    const mimeType = getMimeTypeFromUri(asset.uri);

      // Gera um nome único para a foto
      const nomeFoto = `foto_${idFoto}_${Date.now()}.jpg`;


      // Cria o objeto da nova foto
    const novaFoto = {
      id: idFoto,                // ID único da foto
      uri: asset.uri,            // URI da foto
      base64: asset.base64 || '',// Base64 da foto (se disponível)
      type: mimeType, // Tipo da foto (caso não esteja disponível, define o tipo default como jpeg)
      name: nomeFoto, // Nome da foto (extrai da URI ou cria um nome genérico)
    };

      const novasFotos = [...fotos, novaFoto];
      setFotos(novasFotos);
      onAddFoto(novasFotos); // Passa as novas fotos para o pai
    } else {
      Alert.alert("Limite de fotos", "Você atingiu o limite de 4 fotos.");
    }
  };

  // Função para remover uma foto
  const handleRemoverFoto = (id: string) => {
    setFotos(fotos.filter((foto) => foto.id !== id)); // Remove a foto pelo ID
  };

  const openModal = (uri: string) => {
    setFotoTemp(uri);
    setModalVisible(true);
  };

  const closeModal = () => {
    setModalVisible(false);
    setFotoTemp(null);
  };

  return (
    <View className="mb-6">
      <Text className="text-gray-700 mb-2">Fotos (até 4)</Text>
      <View className="flex-row flex-wrap gap-2">
        {fotos.map((foto) => (
          <View key={foto.id} className="relative w-24 h-24">
            <Pressable onPress={() => openModal(foto.uri)}>
              <Image source={{ uri: foto.uri }} className="w-24 h-24 rounded-md" />
            </Pressable>
            <Pressable
              onPress={() => handleRemoverFoto(foto.id)} // Remove a foto pelo ID
              className="absolute top-0 right-0 bg-black bg-opacity-50 rounded-full p-1"
            >
              <Feather name="x" size={16} color="white" />
            </Pressable>

            {/* Exibir o ID e URI abaixo da foto */}
            <View className="mt-1" style={{ display: 'none' }}>
              <Text className="text-xs text-gray-600">ID: {foto.id}</Text>
              <Text className="text-xs text-gray-600">URI: {foto.uri}</Text>
            </View>
          </View>
        ))}

        {fotos.length < 4 && (
          <View className="flex-row gap-4">
            <Pressable
              onPress={handleFotoEscolher}
              className="w-24 h-24 bg-gray-200 rounded-md items-center justify-center"
            >
              <Feather name="image" size={24} color="#666" />
              <Text className="text-xs text-gray-600 mt-1">Escolher Foto</Text>
            </Pressable>

            <Pressable
              onPress={handleFotoTirar}
              className="w-24 h-24 bg-gray-200 rounded-md items-center justify-center"
            >
              <Feather name="camera" size={24} color="#666" />
              <Text className="text-xs text-gray-600 mt-1">Tirar Foto</Text>
            </Pressable>
          </View>
        )}

        {fotos.length === 4 && (
          <Text className="text-xs text-red-600 mt-2">Você atingiu o limite de 4 fotos</Text>
        )}
      </View>

      {/* Botões para alternar entre câmera frontal e traseira */}
      <View className="mt-4 flex-row justify-center gap-4">
        <TouchableOpacity
          onPress={() => setCameraType(ImagePicker.CameraType.front)} // Altera para a câmera frontal
          className="px-4 py-2 bg-blue-500 rounded-md"
        >
          <Text className="text-white">Câmera Frontal</Text>
        </TouchableOpacity>
        <TouchableOpacity
          onPress={() => setCameraType(ImagePicker.CameraType.back)} // Altera para a câmera traseira
          className="px-4 py-2 bg-blue-500 rounded-md"
        >
          <Text className="text-white">Câmera Traseira</Text>
        </TouchableOpacity>
      </View>

      {/* Modal para visualização da foto em tamanho real */}
      {modalVisible && (
        <Modal
          transparent={true}
          animationType="slide"
          visible={modalVisible}
          onRequestClose={closeModal}
        >
          <View className="flex-1 justify-center items-center bg-black bg-opacity-50">
            <Pressable onPress={closeModal} className="absolute top-0 left-0 right-0 bottom-0" />
            <Pressable onPress={closeModal}>
              <Image
                source={{ uri: fotoTemp }}
                className="w-80 h-80 rounded-md"
              />
            </Pressable>
          </View>
        </Modal>
      )}
    </View>
  );
}
