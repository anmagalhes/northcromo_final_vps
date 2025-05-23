import { useEffect, useState } from 'react';

interface ModalNotificacaoProps {
  visible: boolean;
  onClose: () => void;
  titulo: string;
  mensagem: string;
}

const ModalNotificacao: React.FC<ModalNotificacaoProps> = ({ visible, onClose, titulo, mensagem }) => {
  // Garantir que o modal seja fechado corretamente ao desmontar o componente
  useEffect(() => {
    if (visible) {
      document.body.style.overflow = 'hidden'; // Desabilita o scroll ao abrir o modal
    } else {
      document.body.style.overflow = ''; // Restaura o scroll ao fechar o modal
    }
    return () => {
      document.body.style.overflow = ''; // Garantir que o scroll seja restaurado se o componente for desmontado
    };
  }, [visible]);

  return (
    <div className={`modal-overlay ${visible ? 'visible' : ''}`} onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2 className="titulo">{titulo}</h2>
        <p className="mensagem">{mensagem}</p>
        <button className="botao-fechar" onClick={onClose}>
          Fechar
        </button>
      </div>
      <style jsx>{`
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background-color: rgba(0, 0, 0, 0.5);
          display: none;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }
        .modal-overlay.visible {
          display: flex;
        }
        .modal-content {
          background-color: white;
          padding: 20px;
          border-radius: 10px;
          width: 300px;
          text-align: center;
        }
        .titulo {
          font-size: 18px;
          font-weight: bold;
          margin-bottom: 10px;
        }
        .mensagem {
          font-size: 16px;
          margin-bottom: 20px;
        }
        .botao-fechar {
          background-color: #007bff;
          padding: 10px 20px;
          border-radius: 5px;
          color: white;
          font-size: 16px;
          border: none;
          cursor: pointer;
        }
        .botao-fechar:hover {
          background-color: #0056b3;
        }
      `}</style>
    </div>
  );
};

export default ModalNotificacao;
