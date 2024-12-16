// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Home } from 'pages/home';  // Certifique-se de que Home está corretamente importado
<<<<<<< HEAD
//import { Cliente } from 'pages/cliente'; // Da mesma forma, Cliente deve ser importado corretamente
=======
import { Cliente } from 'pages/Cliente'; // Da mesma forma, Cliente deve ser importado corretamente
>>>>>>> c7cd49eff558732b6b8d14423a5c36ae63633d2c

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

