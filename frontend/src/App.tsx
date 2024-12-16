// src/App.tsx
import React from 'react';
// Components
import Header from 'components/Header/Header';
import Footer from 'components/Footer/Footer';

const App: React.FC = () => {
  return (
    <div>
      <h1>Bem-vindo à aplicação!</h1>
      <Header />
      <h2>TONY!</h2>
      <Footer/>
    </div>
  );
}

export default App;
