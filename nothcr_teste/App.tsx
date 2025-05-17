// App.tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaView } from 'react-native';
import ServiceOrdersScreen from './src/screens/ServiceOrderScreen'; // Corrija o nome conforme necessário
import HomeScreen from './src/screens/HomeScreen'; // Caminho para a HomeScreen
import ServiceOrderDetailsScreen from './src/screens/ServiceOrderDetailsScreen'; // Caminho para a tela de detalhes

const Stack = createStackNavigator();

const App: React.FC = () => {
  return (
    <NavigationContainer>
      <SafeAreaView style={{ flex: 1 }}>
        <Stack.Navigator initialRouteName="Home">
          <Stack.Screen name="Home" component={HomeScreen} />
          <Stack.Screen name="ServiceOrders" component={ServiceOrdersScreen} />
          <Stack.Screen name="ServiceOrderDetails" component={ServiceOrderDetailsScreen} />
        </Stack.Navigator>
      </SafeAreaView>
    </NavigationContainer>
  );
};

export default App;
