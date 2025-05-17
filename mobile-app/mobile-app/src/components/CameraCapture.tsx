// src/components/CameraCapture.tsx
import React, { useRef } from "react";
import { View, Button } from "react-native";
import { Camera } from "expo-camera";

interface Props {
  onPhotoTaken: (uri: string) => void;
}

export const CameraCapture: React.FC<Props> = ({ onPhotoTaken }) => {
  const cameraRef = useRef<Camera | null>(null);

  const takePicture = async () => {
    if (cameraRef.current) {
      const photo = await cameraRef.current.takePictureAsync({ quality: 0.5 });
      onPhotoTaken(photo.uri);
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <Camera style={{ flex: 1 }} ref={cameraRef}>
        <Button title="Capturar Foto" onPress={takePicture} />
      </Camera>
    </View>
  );
};
