// src/api/ordens.ts

import axios from 'axios';
import { Alert } from 'react-native';

interface Foto {
  uri: string;
  base64: string;
  name?: string;
  type?: string;
}

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

export const enviarOrdemComFotos = async (fotos: Foto[], cliente: string) => {
  if (fotos.length === 0) {
    Alert.alert("Nenhuma foto", "Você precisa adicionar pelo menos uma foto.");
    return;
  }

  const formData = new FormData();
  formData.append('cliente', cliente);

  fotos.forEach((foto, index) => {
    const mimeType = foto.type || 'image/jpeg';
    const fileName = foto.name || `foto_${index + 1}.jpg`;
    const blob = base64ToBlob(foto.base64, mimeType);
    const file = new File([blob], fileName, { type: mimeType });

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
      Alert.alert('Sucesso', 'Fotos enviadas com sucesso!\n' + fileLinks.join('\n'));
    } else {
      Alert.alert('Erro', 'Erro ao enviar as fotos');
    }
  } catch (error) {
    console.error("Erro ao enviar fotos:", error);
    Alert.alert('Erro', 'Erro ao enviar as fotos');
  }
};
