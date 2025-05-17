// src/utils/notificacoes.ts
import { Platform } from 'react-native';
import * as Notifications from 'expo-notifications';

// Função para enviar notificação
export const enviarNotificacao = (titulo: string, mensagem: string) => {
  if (Platform.OS !== 'web') { // Verifica se não é Web
    // Dispara notificação usando expo-notifications para dispositivos móveis
    Notifications.scheduleNotificationAsync({
      content: {
        title: titulo,
        body: mensagem,
      },
      trigger: {
        seconds: 1,
      },
    });
  } else {
    // Web - Usa a API de Notificação do navegador
    if ('Notification' in window) {
      // Solicita permissão para exibir notificações no navegador (se necessário)
      if (Notification.permission !== 'granted') {
        Notification.requestPermission().then(permission => {
          if (permission === 'granted') {
            new Notification(titulo, { body: mensagem });
          }
        });
      } else {
        new Notification(titulo, { body: mensagem });
      }
    } else {
      console.warn('Notificações não são suportadas neste navegador.');
    }
  }
};
