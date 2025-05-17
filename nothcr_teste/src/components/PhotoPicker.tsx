import React from 'react';
import { Button, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';

interface PhotoPickerProps {
  onPhotoTaken: (uri: string) => void;  // Callback para passar o URI da foto
}

const PhotoPicker: React.FC<PhotoPickerProps> = ({ onPhotoTaken }) => {
  const pickImage = async () => {
    // Pedir permissão para acessar a câmera
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permissão negada', 'Você precisa permitir o acesso à câmera.');
      return;
    }

    // Abrir a câmera e tirar foto
    const result = await ImagePicker.launchCameraAsync({
      allowsEditing: true,
      quality: 1,
      mediaTypes: ImagePicker.MediaTypeOptions.Images, // Limita para imagens
    });

    if (!result.cancelled) {
      onPhotoTaken(result.uri);  // Passa o URI da foto capturada para o pai
    }
  };

  return <Button title="Tirar Foto" onPress={pickImage} />;
};

export default PhotoPicker;
