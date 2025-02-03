import React from 'react';

const FloatingButtons: React.FC = () => {
  return (
    <div className="floating-buttons">
      <button className="btn" style={{ backgroundColor: '#4caf50', color: 'white' }}>
        <span className="material-icons" style={{ marginRight: 8 }}>save</span>
        Salvar Dados
      </button>
      <button className="btn" style={{ backgroundColor: '#f44336', color: 'white' }}>
        <span className="material-icons" style={{ marginRight: 8 }}>delete</span>
        Excluir Dados
      </button>
      <button className="btn" style={{ backgroundColor: '#2196f3', color: 'white' }}>
        <span className="material-icons" style={{ marginRight: 8 }}>edit</span>
        Editar Dados
      </button>
    </div>
  );
};

export default FloatingButtons;
