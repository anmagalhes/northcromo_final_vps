import React from 'react';
import { MdCloudDownload } from 'react-icons/md'; // <-- Ícone de download

type ButtonGerarPDFsProps = {
  tipo: 'com_pdf' | 'sem_pdf';
  selecionados: number[];
  checklists: {
    id: number;
    recebimento_id: string;
    descricao: string;
    tem_pdf: boolean;
  }[];
  onGenerate: () => void;
};

const ButtonGerarPDFs: React.FC<ButtonGerarPDFsProps> = ({
  tipo, selecionados, checklists, onGenerate
}) => {
  const handleClick = () => {
     // filtra checklists e chama a função do pai
    const checklistsFiltrados = checklists.filter(
      (c) => selecionados.includes(c.id) && (tipo === 'com_pdf' ? c.tem_pdf : !c.tem_pdf)
    );

    console.log(`📄 Gerando PDFs (${tipo}):`, checklistsFiltrados);
    onGenerate();

    // Aqui você coloca a lógica real de geração de PDFs
  };

  return (
    <button
      onClick={handleClick}
      className={`flex items-center justify-center
        bg-green-600 text-white rounded px-4 py-1
        gap-2 hover:bg-green-700
        disabled:bg-green-300 disabled:cursor-not-allowed
        transition-colors duration-300
        focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2
      `}
    >
      <MdCloudDownload className="text-xl" />
      GERAR PDFs ({tipo === 'com_pdf' ? 'com PDF' : 'sem PDF'})
    </button>
  );
};

export default ButtonGerarPDFs;
