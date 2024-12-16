// src/App.tsx
import React from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom'; // React Router

// Components
import Header from  './components/Header/Header';
import Footer from './components/Footer/Flooter';
import Sidebar from './components/Sidebar/Sidebar'

// Importando as rotas
import AppRoutes from './routes/Routes';

// CSS
import styles from "./App.module.css"; // Estilos locais

const App: React.FC = () => {
  return (
    <BrowserRouter>  {/* Contorna a aplicação com o React Router */}
      <div className={styles.appContainer}> {/* Contêiner principal */}

        {/* Cabeçalho */}
        <Header />

        <div className={styles.mainLayout}>  {/* Layout com sidebar e conteúdo */}

          {/* Menu Lateral (Sidebar) */}
          <Sidebar />

          {/* Conteúdo Principal */}
          <main className={styles.mainContent}>  {/* Principal área de conteúdo */}
            <AppRoutes /> {/* Renderiza as rotas */}
          </main>
        </div>

        {/* Rodapé */}
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;