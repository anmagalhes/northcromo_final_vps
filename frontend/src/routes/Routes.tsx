// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Home } from 'pages/home';  // Certifique-se de que Home está corretamente importado
//import { Cliente } from 'pages/cliente'; // Da mesma forma, Cliente deve ser importado corretamente

export const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        {/* Rota para o componente Home */}
        <Route path="/home" element={<Home />} />

        {/* Redirecionamento para /home caso a rota não exista */}
        <Route path="*" element={<Navigate to="/home" />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;

