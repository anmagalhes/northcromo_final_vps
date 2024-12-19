// src/routes/Routes.tsx
import { Routes, Route, Navigate } from 'react-router-dom';
import Home from '../pages/home';
import Cliente from '../pages/cliente';
import { Cliente as ClienteType } from 'src/types'; // Certifique-se de importar o tipo Cliente

export const AppRoutes: React.FC = () => {
  // Função que será passada para o componente Cliente
  const handleClienteAdicionado = (cliente: ClienteType) => {
    console.log('Novo cliente adicionado:', cliente);
    // Aqui você pode fazer o que quiser com o cliente, como atualizar o estado global ou fazer uma requisição para o backend
  };

  return (
    <Routes>
      {/* Rota para a página Home */}
      <Route 
        path="/home" 
        element={<Home />} 
        />

      {/* Rota para a página Cliente */}
      <Route
        path="/cliente"
        element={<Cliente />} 
      />

      {/* Redireciona para /home por padrão */}
      <Route 
        path="*" 
        element={<Navigate to="/home" />} 
        />
    </Routes>
  );
};

export default AppRoutes;
