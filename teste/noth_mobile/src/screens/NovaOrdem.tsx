import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, ScrollView, Image, Alert } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import api from '../services/api';
import ItemInput from '../components/ItemInput';

export default function NovaOrdem() {
  const [clientes, setClientes] = useState([]);
  const [clienteId, setClienteId] = useState('');
  const [descricao, setDescricao] = useState('');
  const [itens, setItens] = useState([{ nome: '', quantidade: '' }]);
  const [fotos, setFotos] = useState([]);

  useEffect(() => {
    api.get('/clientes')
      .then(res => setClientes(res.data))
      .catch(() => Alert.alert('Erro', 'Erro ao buscar clientes'));
  }, []);

  const adicionarItem = () => {
    setItens([...itens, { nome: '', quantidade: '' }]);
  };

  const atualizarItem = (index, campo, valor) => {
    const novosItens = [...itens];
    novosItens[index][campo] = valor;
    setItens(novosItens);
  };

  const escolherImagem = async () => {
    if (fotos.length >= 5) {
      Alert.alert('Limite', 'Máximo de 5 fotos');
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      quality: 0.7,
    });

    if (!result.canceled) {
      setFotos([...fotos, result.assets[0]]);
    }
  };

  const enviarOrdem = async () => {
    if (!clienteId || !descricao) {
      return Alert.alert('Campos obrigatórios', 'Preencha cliente e descrição');
    }

    const formData = new FormData();
    const dadosOrdem = {
      cliente_id: parseInt(clienteId),
      descricao,
      itens: itens.map(item => ({
        nome: item.nome,
        quantidade: parseInt(item.quantidade)
      })),
    };

    formData.append('ordem', JSON.stringify(dadosOrdem));

    fotos.forEach((foto, index) => {
      formData.append('fotos', {
        uri: foto.uri,
        name: `foto-${index + 1}.jpg`,
        type: 'image/jpeg',
      } as any);
    });

    try {
      await api.post('/ordem', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      Alert.alert('Sucesso', 'Ordem enviada com sucesso!');
    } catch (err) {
      console.error(err);
      Alert.alert('Erro', 'Erro ao enviar ordem');
    }
  };

  return (
    <ScrollView contentContainerStyle={{ padding: 20 }}>
      <Text>Cliente:</Text>
      {clientes.map(c => (
        <Button
          key={c.id}
          title={c.nome}
          onPress={() => setClienteId(c.id.toString())}
          color={clienteId == c.id.toString() ? 'green' : 'gray'}
        />
      ))}

      <Text>Descrição:</Text>
      <TextInput
        style={{ borderWidth: 1, marginBottom: 10 }}
        value={descricao}
        onChangeText={setDescricao}
      />

      <Text>Itens:</Text>
      {itens.map((item, index) => (
        <ItemInput
          key={index}
          item={item}
          onUpdate={(campo, valor) => atualizarItem(index, campo, valor)}
        />
      ))}
      <Button title="Adicionar Item" onPress={adicionarItem} />

      <Text>Fotos:</Text>
      <View style={{ flexDirection: 'row', flexWrap: 'wrap' }}>
        {fotos.map((foto, index) => (
          <Image
            key={index}
            source={{ uri: foto.uri }}
            style={{ width: 100, height: 100, margin: 5 }}
          />
        ))}
      </View>
      <Button title="Escolher Imagem" onPress={escolherImagem} />

      <Button title="Enviar Ordem" onPress={enviarOrdem} color="blue" />
    </ScrollView>
  );
}
