// src/screens/ServiceOrderDetailsScreen.tsx
import React from 'react';
import { View, Text, StyleSheet, Button, Alert } from 'react-native';
import { RouteProp } from '@react-navigation/native';

// Tipo de dados de rota
interface ServiceOrderDetailsScreenProps {
  route: RouteProp<{ params: { orderId: string } }, 'params'>;
}

const ServiceOrderDetailsScreen: React.FC<ServiceOrderDetailsScreenProps> = ({ route }) => {
  const { orderId } = route.params;

  // Simulando a busca dos dados da ordem de serviço com base no orderId
  const orderDetails = {
    order_id: orderId,
    vehicle: 'Carro A',
    description: 'Troca de óleo',
    photos: [],
    date_created: '2025-04-19T10:30:00Z',
  };

  const showAlert = () => {
    Alert.alert('Ordem de Serviço', `Você clicou na ordem ${orderId}`);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Detalhes da Ordem de Serviço</Text>
      <Text style={styles.text}>ID da Ordem: {orderDetails.order_id}</Text>
      <Text style={styles.text}>Veículo: {orderDetails.vehicle}</Text>
      <Text style={styles.text}>Descrição: {orderDetails.description}</Text>
      <Text style={styles.text}>Data: {orderDetails.date_created}</Text>

      <Button title="Mostrar Alerta" onPress={showAlert} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  text: {
    fontSize: 16,
    marginVertical: 5,
  },
});

export default ServiceOrderDetailsScreen;
