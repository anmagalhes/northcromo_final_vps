// src/components/ProdutoModal.tsx
import React, { useState } from 'react';
import { Modal, View, Text, FlatList, TextInput, Pressable } from 'react-native';

interface Produto {
  codigo: string;
  nome: string;
}

interface ProdutoModalProps {
  visible: boolean;
  onClose: () => void;
  onSelect: (indice: number) => void;
  produtosDisponiveis: Produto[];
}

export default function ProdutoModal({
  visible,
  onClose,
  onSelect,
  produtosDisponiveis,
}: ProdutoModalProps) {
  const [busca, setBusca] = useState('');

  const filtrados = produtosDisponiveis.filter(
    (item) =>
      item.nome.toLowerCase().includes(busca.toLowerCase()) ||
      item.codigo.includes(busca)
  );

  const handleSelecionar = (produto: Produto) => {
    onSelect(`${produto.codigo} - ${produto.nome}`);
    onClose(); // Fecha automaticamente ao selecionar
    setBusca(''); // Limpa a busca para a próxima vez
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      onRequestClose={onClose}
      transparent={true}
    >
      <View className="flex-1 justify-center items-center bg-black/40">
        <View className="w-11/12 bg-white rounded-lg p-4 max-h-[80%]">
          <Text className="text-lg font-bold mb-2 text-green-700">Selecionar Produto</Text>

          <TextInput
            placeholder="Buscar produto por nome ou código"
            value={busca}
            onChangeText={setBusca}
            className="border border-gray-300 rounded px-3 py-2 mb-3"
          />

        <FlatList
          data={filtrados}
          keyExtractor={(item) => item.codigo}
          renderItem={({ item, index }) => (
            <Pressable
              className="px-3 py-2 border-b border-gray-200"
              onPress={() => {
                const indexOriginal = produtosDisponiveis.findIndex(p => p.codigo === item.codigo);
                onSelect(indexOriginal); // ← Passa o índice original do item na lista completa
                onClose(); // Fecha o modal
                setBusca(''); // Limpa busca
              }}
            >
              <Text>{item.codigo} - {item.nome}</Text>
            </Pressable>
          )}
          ListEmptyComponent={
            <Text className="text-gray-500 text-center mt-2">Nenhum produto encontrado</Text>
          }
        />

          <Pressable
            onPress={onClose}
            className="mt-4 bg-gray-300 rounded px-4 py-2 self-end"
          >
            <Text className="text-gray-800 font-bold">Fechar</Text>
          </Pressable>
        </View>
      </View>
    </Modal>
  );
}
