// src/routes/Routes.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

import Home from '../pages/Home';
import Cliente from '../pages/Cliente';

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Rota para o componente Home */}
      <Route path="/home" element={<Home />} />
      {/* Rota para o componente Cliente */}
      <Route path="/cliente" element={<Cliente />} />

      {/* Redirecionamento para /cliente caso a rota não exista */}
      <Route path="/" element={<Navigate to="/cliente" />} />
    </Routes>
  );
};

export default AppRoutes;
