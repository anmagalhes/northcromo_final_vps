// src/screens/HelloScreen.tsx
import React from 'react';
import { View, Text, Button, Alert, StyleSheet } from 'react-native';

const HelloScreen: React.FC = () => {
  const showHelloAlert = () => {
    Alert.alert('Olá', 'Olá, usuário!');
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tela do Olá</Text>
      <Button title="Mostrar Olá" onPress={showHelloAlert} />
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
    marginBottom: 20,
  },
});

export default HelloScreen;
