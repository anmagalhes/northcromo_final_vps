import React from 'react';
import { FlatList, View, Text, Button } from 'react-native';
import ServiceOrderItem from '../components/ServiceOrderItem'; // Componente que exibe cada ordem

interface HomeScreenProps {
  navigation: any; // Navegação passada como prop
}

const HomeScreen: React.FC<HomeScreenProps> = ({ navigation }) => {
  // Simulando algumas ordens de serviço
  const orders = [
    {
      order_id: 'OS-1234',
      vehicle: 'Carro A',
      description: 'Troca de óleo',
      photos: [],
      date_created: '2025-04-19T10:30:00Z',
    },
    {
      order_id: 'OS-5678',
      vehicle: 'Carro B',
      description: 'Troca de pneus',
      photos: [],
      date_created: '2025-04-20T14:00:00Z',
    },
  ];

  return (
    <View>
      <FlatList
        data={orders}
        keyExtractor={(item) => item.order_id}
        renderItem={({ item }) => (
          <ServiceOrderItem
            order={item}
            onPress={() => navigation.navigate('ServiceOrderDetails', { orderId: item.order_id })}
          />
        )}
      />
    </View>
  );
};

export default HomeScreen;
