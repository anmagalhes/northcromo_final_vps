// src/routes/Routes.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';

<<<<<<< HEAD
//import Home from '../pages/Home';  // Usando o alias
import Cliente from '../pages/cliente';  // Usando o alias
import Home from '../pages/home';
=======
import Home from '../pages/Home';
import Cliente from '../pages/Cliente';
>>>>>>> ec28838e74cf941ebbf337c14de1d521e034ca00

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
