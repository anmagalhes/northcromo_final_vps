// src/screens/NovaOrdem.tsx
import React, { useState } from 'react';
import { View, Text, TextInput, ScrollView, Pressable, Image, Alert } from 'react-native';
import { Feather } from '@expo/vector-icons';

export default function NovaOrdem() {
  const [descricao, setDescricao] = useState('');
  const [itens, setItens] = useState([{ nome: '', quantidade: '' }]);
  const [fotos, setFotos] = useState([]);

  const adicionarItem = () => {
    setItens([...itens, { nome: '', quantidade: '' }]);
  };

  return (
    <ScrollView className="flex-1 bg-slate-100 px-4 py-6">
      <Text className="text-xl font-bold text-green-700 mb-4">Nova Ordem</Text>

      {/* Descrição */}
      <Text className="text-sm font-semibold text-slate-800 mb-1">Descrição:</Text>
      <TextInput
        className="border border-slate-300 rounded-md p-2 bg-white mb-4"
        value={descricao}
        onChangeText={setDescricao}
        placeholder="Digite a descrição"
      />

      {/* Itens */}
      <Text className="text-sm font-semibold text-slate-800 mb-2">Itens:</Text>
      {itens.map((item, index) => (
        <View key={index} className="mb-2 flex-row justify-between space-x-2">
          <TextInput
            className="flex-1 border border-slate-300 rounded-md p-2 bg-white"
            placeholder="Nome do item"
            value={item.nome}
            onChangeText={(text) => {
              const novos = [...itens];
              novos[index].nome = text;
              setItens(novos);
            }}
          />
          <TextInput
            className="w-1/4 border border-slate-300 rounded-md p-2 bg-white"
            placeholder="Qtd"
            keyboardType="numeric"
            value={item.quantidade}
            onChangeText={(text) => {
              const novos = [...itens];
              novos[index].quantidade = text;
              setItens(novos);
            }}
          />
        </View>
      ))}

      <Pressable
        className="bg-green-600 rounded-md p-2 my-2"
        onPress={adicionarItem}
      >
        <Text className="text-white text-center font-bold">+ Adicionar Item</Text>
      </Pressable>

      {/* Fotos */}
      <Text className="text-sm font-semibold text-slate-800 mt-4 mb-2">Fotos:</Text>
      <View className="flex-row flex-wrap gap-2 mb-4">
        {fotos.map((foto, index) => (
          <Image
            key={index}
            source={{ uri: foto.uri }}
            className="w-24 h-24 rounded-md"
          />
        ))}
        {/* Botão para adicionar imagem pode ir aqui */}
      </View>

      {/* Botão Final */}
      <Pressable className="bg-blue-700 rounded-md p-3">
        <Text className="text-white text-center font-bold">Enviar Ordem</Text>
      </Pressable>
    </ScrollView>
  );
}
