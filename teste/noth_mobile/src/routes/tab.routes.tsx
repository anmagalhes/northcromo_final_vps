import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import ListaOrdem from "../app/(drawer)/ListaOrdem";
import NovaOrdem from "../screens/NovaOrdem";

const Tab = createBottomTabNavigator();

export default function TabRoutes() {
  return(
  <Tab.Navigator>
    <Tab.Screen
    name="listaordem"
    component={ListaOrdem}
    />

  <Tab.Screen
      name="novaordem"
      component={NovaOrdem}
      />
  </Tab.Navigator>
  )
}
