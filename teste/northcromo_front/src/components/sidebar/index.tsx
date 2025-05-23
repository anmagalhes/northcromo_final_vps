"use client";
import { useState } from "react";
import { FiMenu, FiHome, FiTruck } from "react-icons/fi";
import Link from "next/link";

export default function Sidebar() {
  const [open, setOpen] = useState(false); // Controle do menu para mobile
  const [expanded, setExpanded] = useState(false); // Controle da expansão/recolhimento no desktop

  return (
    <>
      {/* Botão do menu hambúrguer (aparece apenas em telas pequenas) */}
      <button
        className="p-2 fixed top-6 left-6 z-50 bg-green-600 text-white rounded-full shadow sm:hidden"
        onClick={() => setOpen(!open)} // Alterna a visibilidade da sidebar no mobile
        aria-label="Abrir menu"
      >
        <FiMenu size={20} />
      </button>

      {/* Menu lateral (drawer) para telas pequenas */}
      {open && (
        <aside className="fixed top-0 left-0 w-2/3 h-full bg-white shadow-lg p-6 z-40 sm:hidden flex flex-col gap-4">
          <Link href="/" className="flex items-center gap-2" onClick={() => setOpen(false)}>
            <FiHome />
            Início
          </Link>
          <Link href="/recebimento" className="flex items-center gap-2" onClick={() => setOpen(false)}>
            <FiTruck />
            Recebimento
          </Link>
        </aside>
      )}

      {/* Sidebar fixa para telas grandes */}
      <div
        className={`${
          expanded ? "w-64" : "w-20"
        } hidden sm:block h-full bg-white shadow-lg p-6 fixed top-0 left-0 z-40 transition-all duration-300 ease-in-out`}
      >
        {/* Container para o botão expandir/recolher */}
        <div className="flex justify-between items-center">
          {/* Botão de expandir/recolher a sidebar */}
          <button
            onClick={() => setExpanded(!expanded)} // Alterna entre expandir e recolher
            className="bg-green-600 text-white p-2 rounded-full shadow z-50"
            aria-label="Expandir/Recolher menu"
          >
            {expanded ? (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M10 5L15 10H5L10 5Z" fill="white" />
              </svg>
            ) : (
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 10H15" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            )}
          </button>
        </div>

        {/* Links da Sidebar */}
        <Link href="/" className="flex items-center gap-2 mt-4">
          <FiHome />
          {expanded && "Início"}
        </Link>
        <Link href="/recebimento" className="flex items-center gap-2 mt-4">
          <FiTruck />
          {expanded && "Recebimento"}
        </Link>
      </div>
    </>
  );
}
