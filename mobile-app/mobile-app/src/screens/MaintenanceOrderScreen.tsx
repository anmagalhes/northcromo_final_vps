// src/screens/MaintenanceOrderScreen.tsx
import React from "react";
import { View, Text } from "react-native";
import MaintenanceOrder from "../components/MaintenanceOrder"; // Importa o componente

const MaintenanceOrderScreen = () => {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text style={{ fontSize: 24, marginBottom: 20 }}>Tela de Ordem de Manutenção</Text>
      <MaintenanceOrder />
    </View>
  );
};

export default MaintenanceOrderScreen;
