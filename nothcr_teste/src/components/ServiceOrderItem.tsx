import React from 'react';
import { View, Text, Button, StyleSheet } from 'react-native';

interface ServiceOrderItemProps {
  order: any;
  onPress: () => void;
}

const ServiceOrderItem: React.FC<ServiceOrderItemProps> = ({ order, onPress }) => {
  return (
    <View style={styles.container}>
      <Text>ID da Ordem: {order.order_id}</Text>
      <Text>Veículo: {order.vehicle}</Text>
      <Text>Descrição: {order.description}</Text>
      <Text>Data: {new Date(order.date_created).toLocaleString()}</Text>
      <Button title="Visualizar Detalhes" onPress={onPress} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    marginVertical: 10,
    padding: 10,
    borderWidth: 1,
    borderRadius: 5,
  },
});

export default ServiceOrderItem;
