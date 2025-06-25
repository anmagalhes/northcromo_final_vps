import axios, { AxiosResponse } from 'axios';
import { Alert } from 'react-native';

// Tipo para o retorno da API
interface UploadResponse {
  message: string;
  file_id: string;
  error?: string;
}

// Função de upload de fotos para a API
export const uploadFotosParaAPI = async (
  fotos: string[],  // Fotos são um array de URIs das imagens
  apiUrl: string = 'http://<BACKEND_URL>/upload/'
): Promise<void> => {
  const formData = new FormData();

  // Adicionando as fotos ao FormData
  fotos.forEach((fotoUri, index) => {
    formData.append('file', {
      uri: fotoUri,
      type: 'image/jpeg',  // Ou o tipo correto se não for jpeg
      name: `foto_${index + 1}.jpg`, // Nome único para cada foto
    });
  });

  try {
    // Realizando a requisição POST com o FormData
    const response: AxiosResponse<UploadResponse> = await axios.post(apiUrl, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    // Verificando a resposta da API
    if (response.data.message === 'Upload successful') {
      Alert.alert('Sucesso', `Fotos enviadas com sucesso! ID: ${response.data.file_id}`);
    } else {
      Alert.alert('Erro ao enviar', response.data.error || 'Tente novamente.');
    }
  } catch (error) {
    console.error('Erro ao enviar as fotos:', error);
    Alert.alert('Erro', 'Não foi possível enviar as fotos. Tente novamente.');
  }
};
