// main.tsx
import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';  // Aqui você coloca o Router

import './index.css';
import './styles/styles.css';  // Importe o CSS local

import App from './App';

const rootElement = document.getElementById('root') as HTMLElement;
const root = createRoot(rootElement);  // Criação da raiz para o React 18+

root.render(
  <StrictMode>
    <Router>  {/* O Router é envolvido aqui */}
      <App />
    </Router>
  </StrictMode>
);
