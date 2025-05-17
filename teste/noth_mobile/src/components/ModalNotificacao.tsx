import React, { useState } from 'react';
import { View, Text, Modal, Pressable, StyleSheet } from 'react-native';

// Modal de Notificação
const ModalNotificacao = ({ visible, onClose, titulo, mensagem }: { visible: boolean, onClose: () => void, titulo: string, mensagem: string }) => {
  return (
    <Modal
      transparent
      visible={visible}
      animationType="fade"
      onRequestClose={onClose}
    >
      <View style={styles.modalOverlay}>
        <View style={styles.modalContent}>
          <Text style={styles.titulo}>{titulo}</Text>
          <Text style={styles.mensagem}>{mensagem}</Text>
          <Pressable style={styles.botaoFechar} onPress={onClose}>
            <Text style={styles.botaoTexto}>Fechar</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContent: {
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    width: 300,
    alignItems: 'center',
  },
  titulo: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  mensagem: {
    fontSize: 16,
    marginBottom: 20,
  },
  botaoFechar: {
    backgroundColor: '#007bff',
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 5,
  },
  botaoTexto: {
    color: 'white',
    fontSize: 16,
  },
});

export default ModalNotificacao;
