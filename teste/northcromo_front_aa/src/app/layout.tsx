// src/app/layout.tsx
import type { Metadata } from "next";
import { GeistSans, GeistMono } from "geist/font";
import "./globals.css";

import CoreProvider from "@/components/query_lado_cliente/core-provider";
import AppWrapper from "./AppWrapper";

export const metadata: Metadata = {
  title: "Northcromo - Sistema de Manutenção",
  description: "Sistema de Gestão da Northcromo",
  icons: {
    icon: "/favicon.ico",
  },
  authors: [{ name: "Northcromo" }],
};

export function generateViewport() {
  return {
    themeColor: "#ffffff",
  };
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" className={`${GeistSans.variable} ${GeistMono.variable} h-full`}>
      <body className="antialiased bg-gray-50 min-h-screen flex flex-col overflow-y-auto">
        <CoreProvider>
          <AppWrapper>
            <main className="flex-grow container mx-auto px-4 sm:px-6 lg:px-8">
              {children}
            </main>
          </AppWrapper>
        </CoreProvider>
      </body>
    </html>
  );
}
