// src/pages/Home.tsx
import React from 'react';
import Button from '../components/Button/Button';  // Importando o componente Button

// Definindo o componente
const Home: React.FC = () => {
  const handleClick = () => {
    alert('Botão clicado!');
  };

  return (
    <div>
      <h2>Home Page TONY</h2>
      <Button label="Clique aqui" onClick={handleClick} />
    </div>
  );
};

// Exportando o componente usando export default
export default Home;  // Exportação padrão
