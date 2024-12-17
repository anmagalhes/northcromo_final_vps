// src/components/Sidebar.tsx
import React from 'react';
import { Link } from 'react-router-dom';  // Usando Link para navegação sem recarregar a página

const Sidebar: React.FC = () => {
  return (
    <div className="sidebar">
      <h2>Northcromo</h2>
      <ul>
        <li><Link to="/">Página Inicial</Link></li>
        <li><Link to="/clientes">Clientes</Link></li>
        <li><Link to="/produtos">Produtos</Link></li>
        <li><Link to="/relatorios">Relatórios</Link></li>
        <li><Link to="/configuracoes">Configurações</Link></li>
      </ul>
    </div>
  );
};

export default Sidebar;
