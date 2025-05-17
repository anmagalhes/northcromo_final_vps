// src/app/(drawer)/_layout.tsx
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import { Drawer } from 'expo-router/drawer';
import { Feather } from '@expo/vector-icons';

export default function DrawerLayout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Drawer
        screenOptions={{
          headerShown: false,
          drawerActiveBackgroundColor: '#16a34a', // Cor equivalente ao bg-green-700 no TailwindCSS
          drawerActiveTintColor: 'white',
          drawerStyle: {
            paddingTop:32,
            width:"50%"
          }

        }}>

        <Drawer.Screen
          name="index"
          options={{
            drawerLabel: "Início",
            drawerIcon: ({ color }) => (
              <Feather name="home" size={20} color={color} />
            ),
          }}
        />

      <Drawer.Screen
                name="recebimento"
                options={{
                  drawerLabel: "recebimento",
                  drawerIcon: ({ color }) => (
                    <Feather  name="truck" size={20} color={color} />
                  ),
                }}
              />


        </Drawer>


    </GestureHandlerRootView>
  );
}
