import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css'
import './styles/styles.css';  // Importe o CSS local

import App from './App';

const rootElement = document.getElementById('root') as HTMLElement;
const root = ReactDOM.createRoot(rootElement); // Cria o root usando createRoot

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
