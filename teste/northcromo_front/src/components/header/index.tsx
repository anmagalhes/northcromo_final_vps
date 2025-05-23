"use client";  // Adicione essa linha no início do arquivo

import Link from "next/link";  // Importa Link para navegação interna
import { IoMenu } from "react-icons/io5";  // Ícone de menu
import { FiBell, FiMapPin } from "react-icons/fi";  // Ícones de notificações e localização

// Tipagem para a função que abre o menu (drawer)
const Header: React.FC<{ openDrawer: () => void }> = ({ openDrawer }) => {
  return (
    <div className="w-full flex flex-row items-center justify-between p-4 bg-white shadow-md">
      {/* Ícone de menu */}
      <button
        onClick={openDrawer}  // Aciona a função openDrawer
        className="w-10 h-10 bg-white rounded-full flex justify-center items-center sm:w-12 sm:h-12"
        aria-label="Abrir Menu"
      >
        <IoMenu size={20} className="text-gray-800" />
      </button>

      {/* Título de localização */}
      <div className="flex flex-col items-center justify-center flex-grow sm:flex-row sm:gap-2">
        <span className="text-center text-sm text-slate-800 sm:text-lg">Localização</span>
        <div className="flex-row items-center justify-center gap-1">
          <FiMapPin size={14} className="text-red-600" />
          <span className="text-lg font-bold sm:text-xl">Campo Grande</span>
        </div>
      </div>

      {/* Links de navegação */}
      <div className="flex space-x-4">
        <Link href="/home" className="text-blue-500" aria-current="page">
          Home
        </Link>
        <Link href="/about" className="text-blue-500">
          Sobre
        </Link>
      </div>

      {/* Ícone de notificações */}
      <button
        className="w-10 h-10 bg-white rounded-full flex justify-center items-center sm:w-12 sm:h-12"
        aria-label="Notificações"
      >
        <FiBell size={20} className="text-gray-800" />
      </button>
    </div>
  );
};

export default Header;  // Exporta o componente Header
