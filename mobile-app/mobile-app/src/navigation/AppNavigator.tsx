// src/navigation/AppNavigator.tsx
import React from "react";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { MaintenanceOrderScreen } from "../screens/MaintenanceOrderScreen";

const Stack = createNativeStackNavigator();

export const AppNavigator = () => (
  <NavigationContainer>
    <Stack.Navigator>
      <Stack.Screen name="Ordem de Serviço" component={MaintenanceOrderScreen} />
    </Stack.Navigator>
  </NavigationContainer>
);
