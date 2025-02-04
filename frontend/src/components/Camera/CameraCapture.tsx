import React, { useRef, useState } from 'react';

interface CameraCaptureProps {
  onCapture: (photo: string) => void; // Função para passar a foto para o componente pai
}

const CameraCapture: React.FC<CameraCaptureProps> = ({ onCapture }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [photo, setPhoto] = useState<string | null>(null);

  // Iniciar a câmera
  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      console.error('Erro ao acessar a câmera:', err);
    }
  };

  // Capturar a foto
  const capturePhoto = () => {
    if (canvasRef.current && videoRef.current) {
      const context = canvasRef.current.getContext('2d');
      if (context) {
        canvasRef.current.width = videoRef.current.videoWidth;
        canvasRef.current.height = videoRef.current.videoHeight;
        context.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
        const photoUrl = canvasRef.current.toDataURL('image/png');
        setPhoto(photoUrl); // Armazena a foto como base64
        onCapture(photoUrl); // Passa a foto para o componente pai
      }
    }
  };

  // Limpar a foto
  const clearPhoto = () => {
    setPhoto(null);
    startCamera(); // Reinicia a câmera
  };

  return (
    <div>
      <h3>Captura de Foto</h3>
      <div>
        <video ref={videoRef} autoPlay width="100%" height="auto" />
      </div>
      <button onClick={startCamera}>Iniciar Câmera</button>
      <button onClick={capturePhoto}>Capturar Foto</button>
      <button onClick={clearPhoto}>Limpar Foto</button>

      {photo && (
        <div>
          <h3>Foto Capturada</h3>
          <img src={photo} alt="Captured" width="100%" />
        </div>
      )}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
};

export default CameraCapture;
