// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

import { Home } from '../pages/home'
import { Cliente } from '../pages/cliente';

export const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Rota para o componente Home */}
        <Route path="/home" element={<Home />} />
        
        {/* Rota para o componente Cliente */}
        <Route path="/cliente" element={<Cliente />} />

        {/* Redirecionamento para /home caso a rota não exista */}
        <Route path="*" element={<Navigate to="/cliente" />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
