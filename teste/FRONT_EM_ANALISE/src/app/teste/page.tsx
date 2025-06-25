// src/app/teste/page.tsx
"use client";

// ✅ CERTO – evita hydration mismatch
import dynamic from "next/dynamic";

// 🔧 Aqui importa diretamente com SSR desativado
const CustomTable = dynamic(() => import("@/components/recebimento/teste"), {
  ssr: false,
});

export default function TestePage() {
  return (
    <main className="p-4">
      <h1 className="mb-4 text-2xl font-bold">Teste da Tabela</h1>
      <CustomTable />
    </main>
  );
}
