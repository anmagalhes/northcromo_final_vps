// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/Home'; // Verifique se o caminho está correto e os arquivos existem
import About from '../pages/About'; // Verifique o mesmo aqui

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
