// src/routes/Routes.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from '../pages/Home';  // Corrigido para o caminho correto do arquivo Home.tsx
import Cliente from '../pages/Cliente';  // Corrigido para o caminho correto do arquivo Cliente.tsx

export const AppRoutes: React.FC = () => {
  return (
    <Routes>
      {/* Rota para a página Home */}
      <Route path="/home" element={<Home />} />

      {/* Rota para a página Cliente */}
      <Route path="/cliente" element={<Cliente />} />

      {/* Redireciona para /cliente por padrão */}
      <Route path="/" element={<Navigate to="/cliente" />} />
    </Routes>
  );
};

export default AppRoutes;

