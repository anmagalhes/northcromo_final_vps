// src/screens/MaintenanceOrderScreen.tsx
import React, { useState } from "react";
import { View, Text, Image, ScrollView, Button } from "react-native";
import * as ImagePicker from "expo-image-picker";
import { CameraCapture } from "./CameraCapture";

export const MaintenanceOrderScreen = () => {
  const [photos, setPhotos] = useState<string[]>([]);
  const [showCamera, setShowCamera] = useState(false);

  const handlePhotoTaken = (uri: string) => {
    setPhotos((prev) => [...prev, uri]);
    setShowCamera(false);
  };

  const openCamera = () => {
    if (photos.length >= 4) return;
    setShowCamera(true);
  };

  return (
    <View style={{ flex: 1, padding: 20 }}>
      <Text style={{ fontSize: 24, marginBottom: 10 }}>Ordem de Manutenção</Text>

      {showCamera ? (
        <CameraCapture onPhotoTaken={handlePhotoTaken} />
      ) : (
        <View>
          <Button
            title={`Tirar Foto ${photos.length + 1}`}
            onPress={openCamera}
            disabled={photos.length >= 4}
          />
          <ScrollView horizontal style={{ marginTop: 20 }}>
            {photos.map((uri, index) => (
              <Image
                key={index}
                source={{ uri }}
                style={{ width: 100, height: 100, marginRight: 10 }}
              />
            ))}
          </ScrollView>
        </View>
      )}
    </View>
  );
};
