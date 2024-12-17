// main.tsx
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';  // Usando a versão moderna da React 18+
import './index.css';
import './styles/styles.css';  // Importe o CSS local

import App from './App';

// Criação da raiz para o React 18+
const rootElement = document.getElementById('root') as HTMLElement;
const root = createRoot(rootElement);  // Usando createRoot

root.render(
  <StrictMode>
    <App />
  </StrictMode>
);
