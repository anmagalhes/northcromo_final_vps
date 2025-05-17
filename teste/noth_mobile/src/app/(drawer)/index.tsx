// src/app/home/index.tsx
import React from "react";
import { View, Text, ScrollView } from "react-native";
import Constants from "expo-constants";
import { useNavigation } from "@react-navigation/native";
import { Header } from "../../components/header";

const statusBarHeight = Constants.statusBarHeight;

export default function HomeScreen() {
  const navigation = useNavigation();

  return (
    <ScrollView style={{ flex: 1 }} className="bg-slate-200" showsVerticalScrollIndicator={false}>
      <View className="w-full px-4 bg-green-700" style={{ marginTop: statusBarHeight + 8 }}>
        <Header openDrawer={() => navigation.openDrawer()} />
      </View>

      <View className="px-4 py-6">
        <Text className="text-lg font-bold text-green-700">Bem-vindo à Página Inicial</Text>
      </View>

    </ScrollView>
  );
}
