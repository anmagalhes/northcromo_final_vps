import React from 'react';
import { MdCloudDownload } from 'react-icons/md';
import axios from 'axios';

type ButtonGerarPDFsProps = {
  tipo: 'com_pdf' | 'sem_pdf';
  selecionados: number[];
  checklists: {
    id: number;
    recebimento_id: string;
    descricao: string;
    tem_pdf: boolean;
  }[];
  onGenerate?: () => void; // agora opcional
};

const ButtonGerarPDFs: React.FC<ButtonGerarPDFsProps> = ({
  tipo,
  selecionados,
  checklists,
  onGenerate,
}) => {
  const handleClick = async () => {
    const checklistsFiltrados = checklists.filter(
      (c) => selecionados.includes(c.id) && (tipo === 'com_pdf' ? c.tem_pdf : !c.tem_pdf)
    );

    console.log(`📄 Iniciando geração de PDFs (${tipo}):`, checklistsFiltrados);

    if (tipo === 'sem_pdf') {
      for (const checklist of checklistsFiltrados) {
        try {
          const res = await axios.get(`http://localhost:8000/api/checklist/${checklist.recebimento_id}`);
          console.log(`✅ PDF gerado para recebimento ${checklist.recebimento_id}:`, res.data.link_pdf);
        } catch (err) {
          console.error(`❌ Erro ao gerar PDF para ${checklist.recebimento_id}:`, err);
        }
      }
    } else {
      console.log('📂 Esses já têm PDF. Ações futuras podem ir aqui.');
    }

    if (onGenerate) onGenerate();
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
