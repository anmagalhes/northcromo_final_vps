import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface ServiceOrderDetailsScreenProps {
  route: any; // Dados passados para a tela via navegação
}

const ServiceOrderDetailsScreen: React.FC<ServiceOrderDetailsScreenProps> = ({ route }) => {
  // Pega o ID da ordem de serviço
  const { orderId } = route.params;

  // Aqui você pode buscar os detalhes da ordem de serviço no AsyncStorage ou na API
  const order = {
    order_id: orderId,
    vehicle: 'Carro A',
    description: 'Troca de óleo',
    photos: ['photo1_uri', 'photo2_uri'],
    date_created: '2025-04-19T10:30:00Z',
  };

  return (
    <View style={styles.container}>
      <Text>ID da Ordem: {order.order_id}</Text>
      <Text>Veículo: {order.vehicle}</Text>
      <Text>Descrição: {order.description}</Text>
      <Text>Data de Criação: {new Date(order.date_created).toLocaleString()}</Text>
      {/* Exibe as fotos (se houver) */}
      {order.photos.length > 0 ? (
        <View>
          <Text>Fotos:</Text>
          {order.photos.map((photo, index) => (
            <Text key={index}>{photo}</Text>
          ))}
        </View>
      ) : (
        <Text>Sem fotos</Text>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 20,
  },
});

export default ServiceOrderDetailsScreen;
