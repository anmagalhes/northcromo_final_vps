// src/components/DrawerLayout.tsx
"use client";

import { useState, useEffect } from "react";
import { MdClose } from "react-icons/md";
import Link from "next/link";

const DrawerLayout = () => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleDrawer = () => {
    setIsOpen(!isOpen);
  };

  // Evitar rolagem da página quando o drawer estiver aberto
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden"; // Impede rolagem quando o menu está aberto
      // Mudar o fundo da página quando o drawer estiver aberto
      document.body.style.backgroundColor = "#1F2937"; // Cor de fundo escura
    } else {
      document.body.style.overflow = "";
      document.body.style.backgroundColor = ""; // Restaurar a cor de fundo padrão
    }
  }, [isOpen]);

  return (
    <div className="relative z-50">
      {/* Botão de abrir o menu hamburguer (só visível em dispositivos móveis) */}
      <button
        onClick={toggleDrawer}
        className="fixed top-4 left-4 sm:hidden bg-green-600 text-white p-2 rounded-full shadow z-50"
        aria-label="Abrir menu"
      >
        <svg
          stroke="currentColor"
          fill="currentColor"
          strokeWidth="0"
          viewBox="0 0 24 24"
          height="24"
          width="24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path fill="none" d="M0 0h24v24H0z"></path>
          <path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"></path>
        </svg>
      </button>

      {/* Overlay (fundo escuro) quando o drawer está aberto */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={toggleDrawer} // Fecha o menu ao clicar fora
        />
      )}

      {/* Drawer (menu lateral para dispositivos móveis) */}
      <div
        className={`fixed top-0 left-0 h-full w-64 bg-gray-800 text-white z-50 transform transition-transform duration-300 ease-in-out ${
          isOpen ? "translate-x-0" : "-translate-x-full"
        } sm:translate-x-0 sm:static sm:block`}
      >
        <div className="flex justify-between items-center p-4">
          <h2 className="text-xl font-bold">Northcromo</h2>
          <button onClick={toggleDrawer} className="text-white sm:hidden">
            <MdClose size={24} />
          </button>
        </div>

        {/* Navegação */}
        <nav className="mt-4 space-y-4">
          <Link
            href="/"
            className="flex items-center gap-2 p-3 hover:bg-green-700 rounded"
            onClick={() => setIsOpen(false)}
          >
            <svg
              className="w-5 h-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M3 8h18M3 12h18M3 16h18"
              />
            </svg>
            Início
          </Link>
          <Link
            href="/recebimento"
            className="flex items-center gap-2 p-3 hover:bg-green-700 rounded"
            onClick={() => setIsOpen(false)}
          >
            <svg
              className="w-5 h-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M15 10l4.5-4.5M15 10l4.5 4.5M15 10h6"
              />
            </svg>
            Recebimento
          </Link>
          <Link
            href="/configuracoes"
            className="flex items-center gap-2 p-3 hover:bg-green-700 rounded"
            onClick={() => setIsOpen(false)}
          >
            <svg
              className="w-5 h-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M12 4v16m8-8H4"
              />
            </svg>
            Configurações
          </Link>
        </nav>
      </div>
    </div>
  );
};

export default DrawerLayout;
