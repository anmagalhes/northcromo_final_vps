import React, { useState, useEffect } from 'react';
import { View, Alert, FlatList, ActivityIndicator, TextInput, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import PhotoPicker from '../components/PhotoPicker';  // Componente para capturar a foto
import PhotoGallery from '../components/PhotoGallery';  // Componente para exibir as fotos
import CustomButton from '../components/CustomButton';  // Botão customizado
import ServiceOrderItem from '../components/ServiceOrderItem';  // Componente para exibir cada ordem

interface ServiceOrder {
  order_id: string;
  vehicle: string;
  description: string;
  photos: string[];
  date_created: string;
}

const ServiceOrdersScreen: React.FC = () => {
  const [description, setDescription] = useState('');
  const [photos, setPhotos] = useState<string[]>([]);  // Armazena as fotos tiradas
  const [orders, setOrders] = useState<ServiceOrder[]>([]);  // Armazena as ordens de serviço
  const [loading, setLoading] = useState(false);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const ordersData = await AsyncStorage.getItem('orders');
      if (ordersData) {
        setOrders(JSON.parse(ordersData));
      }
    } catch (error) {
      console.error('Erro ao carregar ordens de serviço:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  const saveServiceOrder = async () => {
    if (!description) {
      Alert.alert('Erro', 'A descrição é obrigatória');
      return;
    }

    const newOrder: ServiceOrder = {
      order_id: `OS-${Math.floor(Math.random() * 10000)}`,
      vehicle: 'Veículo XYZ',
      description,
      photos,
      date_created: new Date().toISOString(),
    };

    const currentOrders = JSON.parse(await AsyncStorage.getItem('orders') || '[]');
    currentOrders.push(newOrder);
    await AsyncStorage.setItem('orders', JSON.stringify(currentOrders));

    Alert.alert('Ordem de Serviço', 'Ordem de serviço criada com sucesso!');
    setDescription('');
    setPhotos([]);
    fetchOrders();
  };

  return (
    <View style={{ padding: 20 }}>
      <TextInput
        placeholder="Descrição da Ordem de Serviço"
        value={description}
        onChangeText={setDescription}
        style={{
          height: 40,
          borderColor: 'gray',
          borderWidth: 1,
          marginBottom: 20,
          paddingLeft: 10,
        }}
      />

      <PhotoPicker onPhotoTaken={(uri) => setPhotos([...photos, uri])} />
      <PhotoGallery photos={photos} />
      <CustomButton title="Salvar Ordem de Serviço" onPress={saveServiceOrder} />

      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <FlatList
          data={orders}
          keyExtractor={(item) => item.order_id}
          renderItem={({ item }) => (
            <ServiceOrderItem
              order={item}
              onPress={() => Alert.alert('Detalhes', JSON.stringify(item))}
            />
          )}
        />
      )}
    </View>
  );
};

export default ServiceOrdersScreen;
