// src/App.tsx
import React from 'react';

// Components
import Header from './components/Header/Header';
import Footer from './components/Footer/Flooter';

//Css
import styles from "./App.module.css";


const App: React.FC = () => {
  return (
    <div>
      <Header />
      <main className={styles.main}>
      <h1>Bem-vindo à aplicaçãAAo!</h1>
      <h2>TESTE!</h2>
      </main>
      <Footer/>
    </div>
  );
}

export default App;