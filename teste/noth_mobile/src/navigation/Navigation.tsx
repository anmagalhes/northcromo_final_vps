import React from 'react';
import { createDrawerNavigator } from '@react-navigation/drawer';
import { NavigationContainer } from '@react-navigation/native';
import NovaOrdem from '../screens/NovaOrdem';  // Tela para criar ordem
import ListaOrdem from '../app/(drawer)/ListaOrdem';  // Tela para listar ordens

const Drawer = createDrawerNavigator();

export default function Navigation() {
  return (
    <NavigationContainer>
      <Drawer.Navigator initialRouteName="ListaOrdem">
        <Drawer.Screen name="Nova Ordem" component={NovaOrdem} />
        <Drawer.Screen name="Lista de Ordens" component={ListaOrdem} />
      </Drawer.Navigator>
    </NavigationContainer>
  );
}
