// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Home } from 'pages/Home';  // Certifique-se de que Home está corretamente importado
import { Cliente } from 'pages/Cliente'; // Da mesma forma, Cliente deve ser importado corretamente

export const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Rota para o componente Home */}
        <Route path="/home" element={<Home />} />
        
        {/* Rota para o componente Cliente */}
        <Route path="/cliente" element={<Cliente />} />

        {/* Redirecionamento para /home caso a rota não exista */}
        <Route path="*" element={<Navigate to="/home" />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
