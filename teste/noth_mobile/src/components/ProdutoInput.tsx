import React, { useState, useEffect } from 'react';
import { View, TextInput, FlatList, Pressable, Text } from 'react-native';
import { Feather } from '@expo/vector-icons';

export default function ProdutoInput({
  produtos,
  codigoProduto,
  setCodigoProduto,
  nomeProduto,
  setNomeProduto,
  abrirModal,
}) {
  const [query, setQuery] = useState('');
  const [sugestoes, setSugestoes] = useState([]);




 // Carrega os produtos ao montar o componente
  useEffect(() => {
    if (!query) {
      setSugestoes([]);
      return;
    }

 // Filtra os produtos com base na consulta
    const filtrados = produtos.filter(
      p =>
        p.codigo.toLowerCase().includes(query.toLowerCase()) ||
        p.nome.toLowerCase().includes(query.toLowerCase())
    );

    setSugestoes(filtrados);
  }, [query]);

  const selecionarProduto = (produto) => {
    setCodigoProduto(produto.codigo);
    setNomeProduto(produto.nome);
    setQuery('');
    setSugestoes([]);
  };

  return (
    <View className="mb-4">
      <Text className="text-gray-700 mb-1">Código do Produto</Text>
      <View className="flex-row items-center border border-gray-300 rounded px-3 py-2 justify-between">
        <TextInput
          className="flex-1 mr-2"
          placeholder="Digite código ou nome"
          value={query || codigoProduto}
          onChangeText={(text) => {
            setQuery(text);
            setCodigoProduto(text);
          }}
        />
        <Pressable onPress={abrirModal}>
          <Feather name="search" size={20} color="#555" />
        </Pressable>
      </View>

      {/* Autocomplete */}
      {sugestoes.length > 0 && (
        <View className="border border-gray-300 rounded mt-1 bg-white shadow-md max-h-40">
          <FlatList
            keyboardShouldPersistTaps="handled"
            data={sugestoes}
            keyExtractor={(item) => item.codigo}
            renderItem={({ item }) => (
              <Pressable
                className="px-3 py-2 border-b border-gray-100"
                onPress={() => selecionarProduto(item)}
              >
                <Text>{item.codigo} - {item.nome}</Text>
              </Pressable>
            )}
          />
        </View>
      )}

      {/* Nome do Produto (readonly) */}
      <Text className="text-gray-700 mt-3 mb-1">Nome do Produto</Text>
      <TextInput
        className="border border-gray-300 rounded px-3 py-2 bg-gray-100 text-gray-700"
        value={nomeProduto}
        editable={false}
      />
    </View>
  );
}
