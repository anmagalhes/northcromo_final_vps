import React from 'react';
import { ScrollView, Image, StyleSheet, Text, View } from 'react-native';

interface PhotoGalleryProps {
  photos: string[];  // Lista de URIs das fotos
}

const PhotoGallery: React.FC<PhotoGalleryProps> = ({ photos }) => {
  // Verificando se há fotos para exibir
  if (photos.length === 0) {
    return (
      <View style={styles.noPhotosContainer}>
        <Text style={styles.noPhotosText}>Nenhuma foto disponível</Text>
      </View>
    );
  }

  return (
    <ScrollView horizontal={true} style={styles.gallery}>
      {photos.map((photoUri, index) => (
        <Image
          key={index}
          source={{ uri: photoUri }}
          style={styles.photo}
          onError={() => console.log('Erro ao carregar a imagem')}  // Log de erro
          resizeMode="cover"
        />
      ))}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  gallery: {
    marginVertical: 10,
  },
  photo: {
    width: 100,
    height: 100,
    marginRight: 10,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#ccc',
  },
  noPhotosContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  noPhotosText: {
    fontSize: 16,
    color: '#888',
  },
});

export default PhotoGallery;
