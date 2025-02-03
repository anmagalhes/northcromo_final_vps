import React, { useState } from 'react';
import Tab1 from '../components/Tab1/Tab1';
import FloatingButtons from '../components/FloatingButtons/FloatingButtons';

const RecebimentoPage: React.FC = () => {
  const [recebimentos, setRecebimentos] = useState<any[]>([]);

  const handleRecebimentoAdicionado = (novoRecebimento: any) => {
    setRecebimentos((prevRecebimentos) => [...prevRecebimentos, novoRecebimento]);
  };

  return (
    <div>
      <h2>Recebimento de Ordens</h2>

      {/* Exibindo a Tab1 com o formulário */}
      <Tab1 onRecebimentoAdicionado={handleRecebimentoAdicionado} />

      {/* Botões flutuantes */}
      <FloatingButtons />
    </div>
  );
};

export default RecebimentoPage;
