// src/app/layout.tsx
"use client";  // Marque este arquivo como um componente de cliente


import { useState } from "react";
import { GeistSans, GeistMono } from "geist/font";
import "./globals.css";  // Estilos globais

import Header from "@/components/header";  // Importa o Header
import Footer from "@/components/Footer";  // Importa o Footer
import Sidebar from "@/components/sidebar";  // Sidebar fixa (opcional)
import DrawerLayout from "@/components/DrawerLayout";  // Drawer para mobile

// Definindo o layout global
export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);

  // Funções para controlar o Drawer (menu móvel)
  const openDrawer = () => setIsDrawerOpen(true);
  const closeDrawer = () => setIsDrawerOpen(false);

// Função para alternar a visibilidade da sidebar
  const toggleSidebar = () => setSidebarAberta(prevState => !prevState);

  return (
    <html lang="pt-BR" className={`${GeistSans.variable} ${GeistMono.variable}`}>
      <body className="antialiased bg-gray-50 min-h-screen flex flex-col">
        {/* Cabeçalho global */}
        <Header openDrawer={openDrawer} />  {/* O Header será incluído globalmente */}

        {/* Conteúdo principal */}
        <div className="flex flex-grow w-full">
          {/* Sidebar fixa para telas grandes */}
          <aside className="hidden sm:block w-64">
            <Sidebar />
          </aside>

          {/* Conteúdo das páginas */}
          <main className="flex-grow container mx-auto p-4">
            {children}  {/* As páginas serão renderizadas aqui */}
          </main>
        </div>

        {/* Drawer para telas pequenas */}
        <div className="sm:hidden">
          <DrawerLayout isOpen={isDrawerOpen} closeDrawer={closeDrawer} />
        </div>

        {/* Rodapé global */}
        <Footer />
      </body>
    </html>
  );
}
