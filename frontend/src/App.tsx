// src/App.tsx
import React from 'react';

// Components
import Header from './components/Header/Header';
import Footer from './components/Footer/Flooter';

const App: React.FC = () => {
  return (
    <div>
      <Header />
      <h1>Bem-vindo à aplicação!</h1>
      <h2>TESTE!</h2>
      <Footer/>
    </div>
  );
}

export default App;