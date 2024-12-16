// src/pages/Home.tsx
import React from 'react';
import Button from '../components/Button/Button'; // Importando o componente Button

export const Home: React.FC = () => {
  const handleClick = () => {
    alert('Botão clicado!');
  };

  return (
    <div>
      <h2>Home Page</h2>
      {/* Adicionando o botão que dispara a função handleClick */}
      <Button label="Clique aqui" onClick={handleClick} />
    </div>
  );
};