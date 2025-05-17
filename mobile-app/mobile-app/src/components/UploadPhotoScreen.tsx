import React, { useState } from 'react';
import { View, Button, Image, StyleSheet, Text } from 'react-native';
import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';

const UploadPhotoScreen: React.FC = () => {
  const [image, setImage] = useState<string | null>(null);  // Armazenando o URI da imagem
  const [uploadStatus, setUploadStatus] = useState<string | null>(null);

  // Função para lidar com a seleção de imagem
  const pickImage = async () => {
    const permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (permissionResult.granted) {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        quality: 1,
      });

      if (!result.canceled && result.assets.length > 0) {
        setImage(result.assets[0].uri);  // Armazena o URI da imagem selecionada
      }
    } else {
      alert("Permissão para acessar a galeria negada!");
    }
  };

  // Função para fazer upload da imagem
  const uploadImage = async () => {
    if (!image) return;

    const formData = new FormData();
    formData.append('file', {
      uri: image,
      name: 'photo.jpg',  // Nome do arquivo pode ser dinâmico
      type: 'image/jpeg', // Tipo da imagem (pode ser ajustado dependendo do tipo de imagem)
    } as any);  // Usando 'as any' para contornar o erro de tipagem

    try {
      const response = await axios.post('http://192.168.1.66:8000/upload/upload-photo/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadStatus(`✅ Upload feito com sucesso: ${response.data.message}`);
      console.log('Upload Response:', response.data);
    } catch (error) {
      console.error('Erro ao fazer upload:', error);
      setUploadStatus('❌ Erro ao fazer upload');
    }
  };

  return (
    <View style={styles.container}>
      {/* Botão para selecionar a imagem */}
      <Button title="Selecionar Imagem" onPress={pickImage} />

      {/* Exibe a imagem selecionada */}
      {image && (
        <Image
          source={{ uri: image }}
          style={styles.image}
        />
      )}

      {/* Botão para enviar a imagem */}
      <Button title="Enviar Imagem" onPress={uploadImage} disabled={!image} />

      {/* Status do upload */}
      {uploadStatus && <Text>{uploadStatus}</Text>}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginTop: 50,
    padding: 20,
  },
  image: {
    width: 250,
    height: 250,
    marginVertical: 20,
  },
});

export default UploadPhotoScreen;
