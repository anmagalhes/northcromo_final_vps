// src/app/inventario/Scanner.tsx
import React, { useState, useEffect } from 'react';
import { View, Text, Button, Alert } from 'react-native';
import { BarCodeScanner } from 'expo-barcode-scanner';

export default function Scanner() {
  const [hasPermission, setHasPermission] = useState<boolean | null>(null);
  const [scanned, setScanned] = useState(false);

  useEffect(() => {
    (async () => {
      const { status } = await BarCodeScanner.requestPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const handleBarCodeScanned = ({ data }: { data: string }) => {
    setScanned(true);
    // Aqui você pode chamar a API ou preencher os campos
    Alert.alert('Código lido', `Conteúdo: ${data}`);
  };

  if (hasPermission === null) return <Text>Solicitando permissão...</Text>;
  if (hasPermission === false) return <Text>Permissão negada</Text>;

  return (
    <View className="flex-1 items-center justify-center">
      <BarCodeScanner
        onBarCodeScanned={scanned ? undefined : handleBarCodeScanned}
        style={{ width: '100%', height: 300 }}
      />
      {scanned && <Button title="Escanear novamente" onPress={() => setScanned(false)} />}
    </View>
  );
}
