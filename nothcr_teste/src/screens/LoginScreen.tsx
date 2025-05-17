import React, { useEffect } from 'react';
import { View, Button, StyleSheet, Text } from 'react-native';
import { GoogleSignin, GoogleSigninButton } from '@react-native-google-signin/google-signin';
import Config from 'react-native-config';  // Importando a configuração do .env
import { useNavigation } from '@react-navigation/native';

export default function LoginScreen() {
  const navigation = useNavigation();

  // Configuração inicial do Google Sign-In
  useEffect(() => {
    GoogleSignin.configure({
      webClientId: Config.WEB_CLIENT_ID,  // Usando a variável do arquivo .env
      offlineAccess: true, // Permite o acesso offline
    });
  }, []);

  // Função para realizar o login com Google
  const signIn = async () => {
    try {
      await GoogleSignin.hasPlayServices();
      const userInfo = await GoogleSignin.signIn();
      console.log(userInfo); // Logando as informações do usuário

      // Após o login, navegue para a tela Home
      navigation.navigate('Home');
    } catch (error) {
      console.error(error);
    }
  };

  // Função para deslogar o usuário
  const signOut = async () => {
    try {
      await GoogleSignin.signOut();
      console.log('Usuário deslogado');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Tela de Login</Text>
      <GoogleSigninButton
        style={{ width: 230, height: 48 }}
        size={GoogleSigninButton.Size.Wide}
        color={GoogleSigninButton.Color.Dark}
        onPress={signIn}
      />
      {/* Botão para deslogar, se necessário */}
      <Button title="Deslogar" onPress={signOut} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
});
