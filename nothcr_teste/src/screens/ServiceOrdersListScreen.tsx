import React, { useEffect, useState } from 'react';
import { View, Text, Button, FlatList, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { ServiceOrder } from '../types/serviceOrder'

const ServiceOrdersListScreen = () => {
  const [orders, setOrders] = useState<ServiceOrder[]>([]);

  // Função para buscar as ordens de serviço do AsyncStorage
  const fetchOrders = async () => {
    try {
      const ordersData = await AsyncStorage.getItem('orders');
      if (ordersData) {
        setOrders(JSON.parse(ordersData));
      }
    } catch (error) {
      console.error('Erro ao carregar ordens de serviço:', error);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const viewOrderDetails = (order: ServiceOrder) => {
    // Aqui você pode navegar para uma tela de detalhes da ordem
    Alert.alert('Detalhes da Ordem', `ID: ${order.order_id}\nDescrição: ${order.description}`);
  };

  return (
    <View style={{ padding: 20 }}>
      <Text style={{ fontSize: 18 }}>Ordens de Serviço</Text>
      <FlatList
        data={orders}
        keyExtractor={(item) => item.order_id}
        renderItem={({ item }) => (
          <View style={{ marginVertical: 10 }}>
            <Text>ID da Ordem: {item.order_id}</Text>
            <Text>Veículo: {item.vehicle}</Text>
            <Text>Descrição: {item.description}</Text>
            <Button title="Visualizar Detalhes" onPress={() => viewOrderDetails(item)} />
          </View>
        )}
      />
    </View>
  );
};

export default ServiceOrdersListScreen;
