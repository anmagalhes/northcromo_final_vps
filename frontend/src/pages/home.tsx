import React from 'react';
import Button from '../components/Button/Button';

const Home: React.FC = () => {
  const handleClick = () => {
    alert('Botão clicado!');
  };

  return (
    <div>
      <h2>Home Page</h2>
      <Button label="Clique aqui" onClick={handleClick} />
    </div>
  );
};

export default Home;
