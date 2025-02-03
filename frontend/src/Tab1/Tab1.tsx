import React from 'react';
import RecebimentoForm from '../RecebimentoForm/RecebimentoForm';

interface Tab1Props {
  onRecebimentoAdicionado: (recebimento: any) => void;
}

const Tab1: React.FC<Tab1Props> = ({ onRecebimentoAdicionado }) => {
  return (
    <div id="tab-1" className="container">
      <RecebimentoForm onRecebimentoAdicionado={onRecebimentoAdicionado} />
    </div>
  );
};

export default Tab1;
