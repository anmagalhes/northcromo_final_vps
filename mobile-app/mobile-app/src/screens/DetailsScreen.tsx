import React, { useState } from 'react';
import {
  View,
  Button,
  Image,
  Text,
  ScrollView,
  StyleSheet,
  TextInput,
  Alert,
  Platform,
} from 'react-native';
import { Camera } from 'expo-camera';
import * as ImagePicker from 'expo-image-picker';
import { uploadPhoto } from '../services/api'; // Importando o serviço de upload

export default function DetailsScreen() {
  const [osNumber, setOsNumber] = useState('');
  const [hasCameraPermission, setHasCameraPermission] = useState<boolean | null>(null);
  const [camera, setCamera] = useState<Camera | null>(null);
  const [photos, setPhotos] = useState<string[]>([]);
  const [showCamera, setShowCamera] = useState(false);

  const requestCameraPermission = async () => {
    const { status } = await Camera.requestCameraPermissionsAsync();
    setHasCameraPermission(status === 'granted');
    setShowCamera(true);
  };

  const requestGalleryPermission = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    return status === 'granted';
  };

  const takePicture = async () => {
    if (camera) {
      const photo = await camera.takePictureAsync();
      setPhotos((prev) => [...prev, photo.uri]);
      setShowCamera(false);
    }
  };

  const pickImageFromGallery = async () => {
    const granted = await requestGalleryPermission();
    if (!granted) {
      Alert.alert('Permissão negada', 'Você precisa permitir acesso à galeria.');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 1,
    });

    if (!result.canceled && result.assets.length > 0) {
      const uri = result.assets[0].uri;
      setPhotos((prev) => [...prev, uri]);
    }
  };

  // Função que salva a OS e envia as fotos
  const saveOrder = async () => {
    if (!osNumber) {
      Alert.alert("Erro", "Digite o número da OS.");
      return;
    }

    if (photos.length === 0) {
      Alert.alert("Erro", "Adicione pelo menos uma foto.");
      return;
    }

    try {
      // Faz o upload de cada foto
      for (const uri of photos) {
        await uploadPhoto(uri, osNumber);  // Chama a função que você definiu para upload
      }

      Alert.alert("Sucesso", `OS ${osNumber} e fotos salvas!`);
      setOsNumber('');
      setPhotos([]);
    } catch (e) {
      Alert.alert("Erro", "Falha ao enviar as fotos.");
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Captura/Upload de Fotos</Text>

      <TextInput
        placeholder="Número da OS"
        value={osNumber}
        onChangeText={setOsNumber}
        style={styles.input}
        keyboardType="numeric"
      />

      {showCamera && hasCameraPermission ? (
        <Camera style={styles.camera} ref={(ref) => setCamera(ref)}>
          <View style={styles.cameraButton}>
            <Button title="📸 Tirar Foto" onPress={takePicture} />
          </View>
        </Camera>
      ) : (
        <>
          <Button
            title="📷 Tirar Foto com Câmera"
            onPress={requestCameraPermission}
            disabled={photos.length >= 4}
          />
          <View style={{ height: 10 }} />
          <Button
            title="🖼️ Escolher da Galeria"
            onPress={pickImageFromGallery}
            disabled={photos.length >= 4}
          />
          <ScrollView horizontal style={styles.photoPreview}>
            {photos.map((uri, idx) => (
              <Image key={idx} source={{ uri }} style={styles.image} />
            ))}
          </ScrollView>
          <Button
            title="💾 Salvar OS e Fotos"
            onPress={saveOrder}  // Chama a função saveOrder aqui
            disabled={!osNumber || photos.length === 0}
          />
        </>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 20 },
  title: { fontSize: 22, marginBottom: 10 },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 6,
    padding: 10,
    marginBottom: 10,
  },
  camera: { flex: 1, justifyContent: 'flex-end' },
  cameraButton: { backgroundColor: 'rgba(0,0,0,0.5)', padding: 10 },
  photoPreview: { marginTop: 20, marginBottom: 20 },
  image: { width: 100, height: 100, marginRight: 10 },
});
