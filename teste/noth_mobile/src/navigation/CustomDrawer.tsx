import React from 'react';
import { View, Text, Pressable } from 'react-native';
import { DrawerContentScrollView, DrawerItemList } from '@react-navigation/drawer';
import { Ionicons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const CustomDrawer = (props: any) => {
  const navigation = useNavigation();

  // Exemplo de função personalizada para navegar de forma personalizada
  const goToCustomPage = () => {
    navigation.navigate('Nova Ordem');
  };

  return (
    <DrawerContentScrollView {...props}>
      {/* Personalização do cabeçalho do menu */}
      <View className="p-4 bg-green-700">
        <Text className="text-white text-xl">Menu de Manutenção</Text>
      </View>

      {/* Lista personalizada de opções */}
      <View className="mt-4">
        <Pressable
          onPress={goToCustomPage}
          className="flex flex-row items-center p-3 bg-white rounded-lg mb-2 shadow-md"
        >
          <Ionicons name="add-circle" size={20} color="green" />
          <Text className="ml-2 text-green-700">Nova Ordem de Manutenção</Text>
        </Pressable>

        <Pressable
          onPress={() => navigation.navigate('Lista de Ordens')}
          className="flex flex-row items-center p-3 bg-white rounded-lg mb-2 shadow-md"
        >
          <Ionicons name="list" size={20} color="green" />
          <Text className="ml-2 text-green-700">Lista de Ordens</Text>
        </Pressable>

        {/* Adicione outras opções personalizadas aqui */}
        <Pressable
          onPress={() => navigation.navigate('Configurações')}
          className="flex flex-row items-center p-3 bg-white rounded-lg mb-2 shadow-md"
        >
          <Ionicons name="settings" size={20} color="green" />
          <Text className="ml-2 text-green-700">Configurações</Text>
        </Pressable>
      </View>

      {/* Opcional: Você pode incluir a lista padrão do Drawer para navegação */}
      <DrawerItemList {...props} />
    </DrawerContentScrollView>
  );
};

export default CustomDrawer;
