// src/app/settings/index.tsx
import React from "react";
import { View, Text, Button } from "react-native";
import { useRouter } from "expo-router";  // Hook para navegação

export default function SettingsScreen() {
  const router = useRouter();

  return (
    <View>
      <Text>Configurações</Text>
      <Button title="Voltar para a Home" onPress={() => router.back()} />
    </View>
  );
}
