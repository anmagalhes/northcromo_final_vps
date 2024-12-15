// src/routes/Routes.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from '../pages/home'; 
import Cliente from '../pages/clientes'; 

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/" element={<Cliente />} />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
